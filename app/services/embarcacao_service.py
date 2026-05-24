from __future__ import annotations

from typing import Any

from app.repositories.embarcacao_repository import EmbarcacaoRepository
from app.utils.serializers import audit_fields, parse_bool, parse_decimal, parse_float, parse_int, text_or_none


class EmbarcacaoService:
    def build_payload(self, form, user_id: str | None, pescador_id: str | None = None) -> dict[str, Any]:
        return {
            "pescador_id": pescador_id,
            "pesca_embarcada": parse_bool(form.get("pesca_embarcada")),
            "embarcacao_propria": parse_bool(form.get("embarcacao_propria")),
            "status_financeiro": text_or_none(form.get("status_financeiro")),
            "nome_proprietario": text_or_none(form.get("nome_proprietario")),
            "apelido_proprietario": text_or_none(form.get("apelido_proprietario")),
            "cilindros_hp": parse_float(form.get("cilindros_hp")),
            "porto_origem": text_or_none(form.get("porto_origem")),
            "porto_desembarque": text_or_none(form.get("porto_desembarque")),
            "nome_embarcacao": text_or_none(form.get("nome_embarcacao")),
            "comprimento_m": parse_float(form.get("comprimento_m")),
            "num_registro": text_or_none(first_non_empty(form.get("num_registro"), form.get("numero_registro"))),
            "largura_m": parse_float(form.get("largura_m")),
            "tonelada_bruta_ab": parse_float(form.get("tonelada_bruta_ab", form.get("tonelada_bruta", ""))),
            "material_casco": text_or_none(form.get("material_casco")),
            "capacidade_tripulacao": parse_int(form.get("capacidade_tripulacao")),
            "ano_construcao": parse_int(form.get("ano_construcao")),
            "registro_capitania": parse_bool(form.get("registro_capitania")),
            "registro_rgp": parse_bool(form.get("registro_rgp")),
            "licenciamento_ibama": parse_bool(form.get("licenciamento_ibama")),
            "licenciamento_mpa": parse_bool(form.get("licenciamento_mpa")),
            "tipo_embarcacao": text_or_none(form.get("tipo_embarcacao")),
            **audit_fields(user_id),
        }

    def save(self, client: Any, form, user_id: str | None, pescador_id: str | None):
        embarcacao_repo = EmbarcacaoRepository(client)
        embarcacao_payload = self.build_payload(form, user_id, pescador_id)
        embarcacao_response = embarcacao_repo.create(embarcacao_payload)
        embarcacao_id = self._extract_id(embarcacao_response)

        try:
            propulsao_values = form.getlist("embarcacao_propulsao")
            propulsao_rows = [
                {"embarcacao_id": embarcacao_id, "tipo_propulsao": value}
                for value in propulsao_values
                if str(value).strip()
            ]
            embarcacao_repo.create_propulsao(propulsao_rows)
        except Exception:
            embarcacao_repo.delete(embarcacao_id)
            raise

        return embarcacao_id

    def _extract_id(self, response):
        data = getattr(response, "data", None)
        if isinstance(data, list) and data:
            row = data[0]
            if isinstance(row, dict):
                return row.get("id")
        return None
