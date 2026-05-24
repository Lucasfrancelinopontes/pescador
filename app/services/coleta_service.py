from __future__ import annotations

from uuid import uuid4
from typing import Any

from app.repositories.coleta_repository import ColetaRepository
from app.services.embarcacao_service import EmbarcacaoService
from app.services.pescador_service import PescadorService
from app.utils.serializers import audit_fields, first_non_empty, parse_date, parse_int, text_or_none


class ColetaService:
    def build_payload(self, client: Any, form, user_id: str | None) -> dict[str, Any]:
        municipio_id = self._resolve_municipio_id(client, form)
        localidade_id = self._resolve_localidade_id(client, form, municipio_id)
        return {
            "codigo_coleta": self._build_codigo_coleta(form),
            "codigo_foto": text_or_none(form.get("codigo_foto")),
            "municipio_id": municipio_id,
            "localidade_id": localidade_id,
            "coletor_id": self._lookup_id(client, "coletores", form.get("coletor"), ("nome",)),
            "digitador_id": self._lookup_id(client, "digitadores", form.get("digitador"), ("nome",)),
            "data_coleta": parse_date(first_non_empty(form.get("data_coleta"), form.get("data"))),
            "data_digitacao": parse_date(first_non_empty(form.get("data_digitacao"), form.get("data_digitador"))),
            "observacoes": text_or_none(form.get("observacoes")),
            **audit_fields(user_id),
        }

    def submit_complete(self, client: Any, form, user_id: str | None) -> dict[str, Any]:
        coleta_repo = ColetaRepository(client)
        pescador_service = PescadorService()
        embarcacao_service = EmbarcacaoService()

        created_ids: dict[str, Any] = {"coleta_id": None, "pescador_id": None, "embarcacao_id": None}
        try:
            coleta_response = coleta_repo.create(self.build_payload(client, form, user_id))
            coleta_id = self._extract_id(coleta_response)
            created_ids["coleta_id"] = coleta_id

            pescador_id = pescador_service.save(client, form, user_id, coleta_id)
            created_ids["pescador_id"] = pescador_id

            embarcacao_id = embarcacao_service.save(client, form, user_id, pescador_id)
            created_ids["embarcacao_id"] = embarcacao_id
        except Exception:
            self._rollback(client, created_ids)
            raise

        return created_ids

    def _rollback(self, client: Any, created_ids: dict[str, Any]) -> None:
        coleta_repo = ColetaRepository(client)
        pescador_repo = __import__("app.repositories.pescador_repository", fromlist=["PescadorRepository"]).PescadorRepository(client)
        embarcacao_repo = __import__("app.repositories.embarcacao_repository", fromlist=["EmbarcacaoRepository"]).EmbarcacaoRepository(client)

        # Futuras transações reais podem substituir esta reversão lógica.
        try:
            if created_ids.get("embarcacao_id"):
                embarcacao_repo.delete(created_ids["embarcacao_id"])
        except Exception:
            pass
        try:
            if created_ids.get("pescador_id"):
                pescador_repo.delete(created_ids["pescador_id"])
        except Exception:
            pass
        try:
            if created_ids.get("coleta_id"):
                coleta_repo.delete(created_ids["coleta_id"])
        except Exception:
            pass

    def _extract_id(self, response):
        data = getattr(response, "data", None)
        if isinstance(data, list) and data:
            row = data[0]
            if isinstance(row, dict):
                return row.get("id")
        return None

    def _build_codigo_coleta(self, form) -> str:
        codigo_coleta = text_or_none(form.get("codigo_coleta"))
        if codigo_coleta:
            return codigo_coleta
        return uuid4().hex

    def _resolve_municipio_id(self, client: Any, form) -> int | None:
        municipio_id = parse_int(form.get("municipio_id"))
        if municipio_id is not None:
            return municipio_id
        return self._lookup_id(client, "municipios", form.get("municipio"), ("nome", "codigo"))

    def _resolve_localidade_id(self, client: Any, form, municipio_id: int | None) -> int | None:
        localidade_id = parse_int(form.get("localidade_id"))
        if localidade_id is not None:
            return localidade_id

        localidade = text_or_none(form.get("localidade"))
        if not localidade:
            return None

        if municipio_id is not None:
            for column in ("nome", "codigo"):
                try:
                    response = (
                        client.table("localidades")
                        .select("id")
                        .eq("municipio_id", municipio_id)
                        .eq(column, localidade)
                        .limit(1)
                        .execute()
                    )
                except Exception:
                    continue
                resolved_id = self._extract_id(response)
                if resolved_id is not None:
                    return resolved_id

        return self._lookup_id(client, "localidades", localidade, ("nome", "codigo"))

    def _lookup_id(self, client: Any, table_name: str, value, columns: tuple[str, ...]) -> int | str | None:
        text = text_or_none(value)
        if not text:
            return None

        for column in columns:
            try:
                response = client.table(table_name).select("id").eq(column, text).limit(1).execute()
            except Exception:
                continue
            resolved_id = self._extract_id(response)
            if resolved_id is not None:
                return resolved_id
        return None
