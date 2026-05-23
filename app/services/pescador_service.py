from __future__ import annotations

import json
from typing import Any

from app.repositories.embarcacao_repository import EmbarcacaoRepository
from app.repositories.pescador_repository import PescadorRepository
from app.utils.serializers import (
    audit_fields,
    ensure_list,
    first_non_empty,
    parse_bool,
    parse_date,
    parse_decimal,
    parse_float,
    parse_int,
)


class PescadorService:
    def build_payload(self, form, user_id: str | None, coleta_id: str | None = None) -> dict[str, Any]:
        return {
            "coleta_id": coleta_id,
            "nome": first_non_empty(form.get("nome"), default=""),
            "apelido": form.get("apelido", "").strip(),
            "telefone": form.get("telefone", "").strip(),
            "sexo": form.get("sexo", "").strip(),
            "data_nascimento": parse_date(first_non_empty(form.get("data_nascimento"), form.get("nascimento"))),
            "naturalidade": form.get("naturalidade", "").strip(),
            "estado_civil": form.get("estado_civil", "").strip(),
            "atividade_principal_renda": form.get("atividade_principal_renda", "").strip(),
            "atividade_secundaria_renda": form.get("atividade_secundaria_renda", "").strip(),
            "composicao_familiar_num": parse_int(first_non_empty(form.get("composicao_familiar_num"), form.get("composicao_familiar"))),
            "escolaridade": form.get("escolaridade", "").strip(),
            "local_moradia": form.get("local_moradia", form.get("moradia_comunidade_tradicional", "")).strip(),
            "local_moradia_outro": form.get("local_moradia_outro", form.get("moradia_outro", "")).strip(),
            "tipo_construcao": form.get("tipo_construcao", "").strip(),
            "tipo_construcao_outro": form.get("tipo_construcao_outro", "").strip(),
            "saude_vista": parse_bool(first_non_empty(form.get("saude_vista"), form.get("vista"))),
            "saude_pele": parse_bool(first_non_empty(form.get("saude_pele"), form.get("pele"))),
            "saude_coluna": parse_bool(first_non_empty(form.get("saude_coluna"), form.get("coluna"))),
            "saude_ginecologico": parse_bool(first_non_empty(form.get("saude_ginecologico"), form.get("ginecologico"))),
            "saude_outros": form.get("saude_outros", form.get("saude_outros_texto", "")).strip(),
            "registro_inss": form.get("registro_inss", "").strip(),
            "registro_colonia": form.get("registro_colonia", "").strip(),
            "nome_colonia": form.get("nome_colonia", form.get("qual_colonia", "")).strip(),
            "registro_associacao": form.get("registro_associacao", "").strip(),
            "nome_associacao": form.get("nome_associacao", form.get("qual_associacao", "")).strip(),
            "possui_carteira_pescador": parse_bool(form.get("possui_carteira_pescador")),
            "tipo_carteira": form.get("tipo_carteira", "").strip(),
            "tempo_na_atividade": form.get("tempo_na_atividade", form.get("tempo_atividade", "")).strip(),
            "horas_trabalho_dia": parse_float(first_non_empty(form.get("horas_trabalho_dia"), form.get("horas_por_dia"))),
            "principais_fontes_renda_familiar": form.get("principais_fontes_renda_familiar", form.get("fontes_renda_familiar", "")).strip(),
            "categoria_pesca": form.get("categoria_pesca", "").strip(),
            "principal_pescaria_pescado": form.get("principal_pescaria_pescado", form.get("principal_pescaria", "")).strip(),
            "petrecho_nome": form.get("petrecho_nome", form.get("petrecho_pesca", "")).strip(),
            "petrecho_tamanho_m": parse_float(first_non_empty(form.get("petrecho_tamanho_m"), form.get("tamanho_metros"))),
            "petrecho_tamanho_bracas": parse_float(first_non_empty(form.get("petrecho_tamanho_bracas"), form.get("tamanho_bracas"))),
            "petrecho_unidades": parse_int(first_non_empty(form.get("petrecho_unidades"), form.get("unidades"))),
            "petrecho_material": form.get("petrecho_material", form.get("material_petrecho", "")).strip(),
            "tipo_iscas": form.get("tipo_iscas", "").strip(),
            "processo_lancamento_recolhimento": form.get("processo_lancamento_recolhimento", "").strip(),
            "quadrantes_mapa": self._parse_quadrantes(form),
            "media_dias_embarcado": parse_int(form.get("media_dias_embarcado")),
            "viagens_por_mes": parse_int(form.get("viagens_por_mes")),
            "producao_media_viagem_kg": parse_float(first_non_empty(form.get("producao_media_viagem_kg"))),
            "producao_media_viagem_unidades": parse_int(first_non_empty(form.get("producao_media_viagem_unidades"), form.get("producao_media_unidades"))),
            "valor_medio_kg_primeira_qualidade": parse_decimal(first_non_empty(form.get("valor_medio_kg_primeira_qualidade"), form.get("valor_primeira_qualidade"))),
            "valor_medio_kg_segunda_qualidade": parse_decimal(first_non_empty(form.get("valor_medio_kg_segunda_qualidade"), form.get("valor_segunda_qualidade"))),
            "valor_medio_kg_terceira_qualidade": parse_decimal(first_non_empty(form.get("valor_medio_kg_terceira_qualidade"), form.get("valor_terceira_qualidade"))),
            "renda_media_mensal": parse_decimal(form.get("renda_media_mensal")),
            "renda_media_por_pescaria": parse_decimal(first_non_empty(form.get("renda_media_por_pescaria"), form.get("renda_por_pescaria"))),
            "petrechos_proprios": parse_bool(form.get("petrechos_proprios")),
            "petrechos_proprietario_se_nao": form.get("petrechos_proprietario_se_nao", form.get("petrechos_de_quem", "")).strip(),
            "como_conserva_pescado": form.get("como_conserva_pescado", form.get("conservacao_pescado", "")).strip(),
            "entrega_atravessador": parse_bool(first_non_empty(form.get("entrega_atravessador"))),
            "divida_com_atravessador": parse_bool(first_non_empty(form.get("divida_com_atravessador"), form.get("dividaAtravessador"))),
            "percepcao_pesca_passado": form.get("percepcao_pesca_passado", form.get("percepcao_pesca_hoje_vs_passado", "")).strip(),
            "percepcao_tamanho_volume_capturado": form.get("percepcao_tamanho_volume_capturado", form.get("percepcao_tamanho_volume_pescado", "")).strip(),
            **audit_fields(user_id),
        }

    def save(self, client: Any, form, user_id: str | None, coleta_id: str | None):
        pescador_repo = PescadorRepository(client)
        embarcacao_repo = EmbarcacaoRepository(client)
        pescador_payload = self.build_payload(form, user_id, coleta_id)
        pescador_response = pescador_repo.create(pescador_payload)
        pescador_id = self._extract_id(pescador_response)

        try:
            relacoes = self._build_relacao_trabalho_rows(form, pescador_id)
            pescador_repo.create_relacao_trabalho(relacoes)

            pescados = self._build_pescados_rows(form, pescador_id)
            pescador_repo.create_pescados_safra(pescados)

            despesas = self._build_despesas_rows(form, pescador_id)
            pescador_repo.create_despesas_atividade(despesas)
        except Exception:
            pescador_repo.delete(pescador_id)
            raise

        return pescador_id

    def _build_relacao_trabalho_rows(self, form, pescador_id: str) -> list[dict[str, Any]]:
        values = form.getlist("tipo_relacao_trabalho") or form.getlist("relacao_trabalho")
        return [
            {"pescador_id": pescador_id, "relacao_trabalho": value}
            for value in values
            if str(value).strip()
        ]

    def _build_pescados_rows(self, form, pescador_id: str) -> list[dict[str, Any]]:
        payload = form.get("pescados_safra")
        if payload:
            parsed = json.loads(payload)
            return [
                {
                    "pescador_id": pescador_id,
                    "nome_comum": item.get("nome_comum", "").strip(),
                    "inicio_safra": item.get("inicio_safra") or None,
                    "fim_safra": item.get("fim_safra") or None,
                }
                for item in parsed
                if item.get("nome_comum")
            ]
        return []

    def _build_despesas_rows(self, form, pescador_id: str) -> list[dict[str, Any]]:
        payload = form.get("despesas_atividade")
        if payload:
            parsed = json.loads(payload)
            rows: list[dict[str, Any]] = []
            for item in parsed:
                if not str(item.get("item_despesa", "")).strip():
                    continue
                rows.append(
                    {
                        "pescador_id": pescador_id,
                        "item_despesa": item.get("item_despesa", "").strip(),
                        "tipo": item.get("tipo", "").strip(),
                        "quantidade": parse_float(item.get("quantidade")),
                        "unidade": item.get("unidade", "").strip(),
                        "custo_reais": parse_decimal(item.get("custo_reais")),
                        "outros": item.get("outros", "").strip(),
                        "frequencia": item.get("frequencia", "").strip(),
                    }
                )
            return rows
        return []

    def _parse_quadrantes(self, form) -> list[str]:
        hidden = form.get("quadrantes_mapa")
        if hidden:
            try:
                parsed = json.loads(hidden)
                return [str(item).strip() for item in parsed if str(item).strip()]
            except Exception:
                pass
        return [
            value.strip()
            for key in ["quadrante_1", "quadrante_2", "quadrante_3", "quadrante_4", "quadrante_5"]
            for value in [form.get(key, "")]
            if value.strip()
        ]

    def _extract_id(self, response):
        data = getattr(response, "data", None)
        if isinstance(data, list) and data:
            row = data[0]
            if isinstance(row, dict):
                return row.get("id")
        return None
