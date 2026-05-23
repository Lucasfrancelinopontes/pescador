from __future__ import annotations

from typing import Any

from app.repositories.coleta_repository import ColetaRepository
from app.services.embarcacao_service import EmbarcacaoService
from app.services.pescador_service import PescadorService
from app.utils.serializers import audit_fields, parse_date, first_non_empty


class ColetaService:
    def build_payload(self, form, user_id: str | None) -> dict[str, Any]:
        return {
            "codigo_coleta": form.get("codigo_coleta", "").strip(),
            "codigo_foto": form.get("codigo_foto", "").strip(),
            "municipio_id": form.get("municipio_id", form.get("municipio", "")).strip(),
            "localidade_id": form.get("localidade_id", form.get("localidade", "")).strip(),
            "data_coleta": parse_date(first_non_empty(form.get("data_coleta"), form.get("data"))),
            "data_digitacao": parse_date(first_non_empty(form.get("data_digitacao"), form.get("data_digitador"))),
            "observacoes": form.get("observacoes", "").strip(),
            **audit_fields(user_id),
        }

    def submit_complete(self, client: Any, form, user_id: str | None) -> dict[str, Any]:
        coleta_repo = ColetaRepository(client)
        pescador_service = PescadorService()
        embarcacao_service = EmbarcacaoService()

        created_ids: dict[str, Any] = {"coleta_id": None, "pescador_id": None, "embarcacao_id": None}
        try:
            coleta_response = coleta_repo.create(self.build_payload(form, user_id))
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
