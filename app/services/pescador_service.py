from __future__ import annotations

import json
from typing import Any

from app.repositories.embarcacao_repository import EmbarcacaoRepository
from app.repositories.pescador_repository import PescadorRepository
from app.utils.serializers import (
    audit_fields,
    ensure_list,
    first_non_empty,
    normalize_enum_text,
    parse_bool,
    parse_date,
    parse_decimal,
    parse_float,
    parse_int,
    text_or_none,
)


class PescadorService:
    def build_payload(self, form, user_id: str | None, coleta_id: str | None = None) -> dict[str, Any]:
        return {
            "coleta_id": coleta_id,
            "nome": text_or_none(first_non_empty(form.get("nome"), default="")),
            "apelido": text_or_none(form.get("apelido")),
            "telefone": text_or_none(form.get("telefone")),
            "sexo": text_or_none(form.get("sexo")),
            "data_nascimento": parse_date(first_non_empty(form.get("data_nascimento"), form.get("nascimento"))),
            "naturalidade": text_or_none(form.get("naturalidade")),
            "estado_civil": text_or_none(form.get("estado_civil")),
            "atividade_principal_renda": text_or_none(form.get("atividade_principal_renda")),
            "atividade_secundaria_renda": text_or_none(form.get("atividade_secundaria_renda")),
            "composicao_familiar_num": parse_int(first_non_empty(form.get("composicao_familiar_num"), form.get("composicao_familiar"))),
            "escolaridade": text_or_none(form.get("escolaridade")),
            "local_moradia": text_or_none(first_non_empty(form.get("local_moradia"), form.get("moradia_comunidade_tradicional"))),
            "local_moradia_outro": text_or_none(first_non_empty(form.get("local_moradia_outro"), form.get("moradia_outro"))),
            "tipo_construcao": text_or_none(form.get("tipo_construcao")),
            "tipo_construcao_outro": text_or_none(form.get("tipo_construcao_outro")),
            "saude_vista": parse_bool(first_non_empty(form.get("saude_vista"), form.get("vista"))),
            "saude_pele": parse_bool(first_non_empty(form.get("saude_pele"), form.get("pele"))),
            "saude_coluna": parse_bool(first_non_empty(form.get("saude_coluna"), form.get("coluna"))),
            "saude_ginecologico": parse_bool(first_non_empty(form.get("saude_ginecologico"), form.get("ginecologico"))),
            "saude_outros": text_or_none(first_non_empty(form.get("saude_outros"), form.get("saude_outros_texto"))),
            "registro_inss": parse_bool(form.get("registro_inss")),
            "registro_colonia": parse_bool(form.get("registro_colonia")),
            "nome_colonia": text_or_none(first_non_empty(form.get("nome_colonia"), form.get("qual_colonia"))),
            "registro_associacao": parse_bool(form.get("registro_associacao")),
            "nome_associacao": text_or_none(first_non_empty(form.get("nome_associacao"), form.get("qual_associacao"))),
            "possui_carteira_pescador": parse_bool(form.get("possui_carteira_pescador")),
            "tipo_carteira": normalize_enum_text(
                first_non_empty(
                    form.get("tipo_carteira"),
                    "grande_marinha" if text_or_none(form.get("carteira_grande_marinha")) else None,
                    "pequena_colonia" if text_or_none(form.get("carteira_pequena_colonia")) else None,
                )
            ),
            "tempo_na_atividade": text_or_none(first_non_empty(form.get("tempo_na_atividade"), form.get("tempo_atividade"))),
            "horas_trabalho_dia": parse_float(first_non_empty(form.get("horas_trabalho_dia"), form.get("horas_por_dia"))),
            "principais_fontes_renda_familiar": text_or_none(first_non_empty(form.get("principais_fontes_renda_familiar"), form.get("fontes_renda_familiar"))),
            "categoria_pesca": self._normalize_categoria_pesca(form.get("categoria_pesca")),
            "principal_pescaria_pescado": text_or_none(first_non_empty(form.get("principal_pescaria_pescado"), form.get("principal_pescaria"))),
            "petrecho_nome": text_or_none(first_non_empty(form.get("petrecho_nome"), form.get("petrecho_pesca"))),
            "petrecho_tamanho_m": parse_float(first_non_empty(form.get("petrecho_tamanho_m"), form.get("tamanho_metros"))),
            "petrecho_tamanho_bracas": parse_float(first_non_empty(form.get("petrecho_tamanho_bracas"), form.get("tamanho_bracas"))),
            "petrecho_unidades": parse_int(first_non_empty(form.get("petrecho_unidades"), form.get("unidades"))),
            "petrecho_material": text_or_none(first_non_empty(form.get("petrecho_material"), form.get("material_petrecho"))),
            "tipo_iscas": text_or_none(form.get("tipo_iscas")),
            "processo_lancamento_recolhimento": text_or_none(form.get("processo_lancamento_recolhimento")),
            "quadrantes_mapa": self._parse_quadrantes(form),
            "media_dias_embarcado": parse_int(form.get("media_dias_embarcado")),
            "viagens_por_mes": parse_int(form.get("viagens_por_mes")),
            "producao_media_viagem_kg": parse_float(first_non_empty(form.get("producao_media_viagem_kg"))),
            "producao_media_viagem_unidades": parse_int(first_non_empty(form.get("producao_media_viagem_unidades"), form.get("producao_media_unidades"))),
            "valor_medio_kg_primeira_qualidade": parse_decimal(first_non_empty(form.get("valor_medio_kg_primeira_qualidade"), form.get("valor_primeira_qualidade"))),
            "valor_medio_kg_segunda_qualidade": parse_decimal(first_non_empty(form.get("valor_medio_kg_segunda_qualidade"), form.get("valor_segunda_qualidade"))),
            "valor_medio_kg_terceira_qualidade": parse_decimal(first_non_empty(form.get("valor_medio_kg_terceira_qualidade"), form.get("valor_terceira_qualidade"))),
            "renda_media_mensal": parse_decimal(first_non_empty(form.get("renda_media_mensal"), form.get("renda_mensal"))),
            "renda_media_por_pescaria": parse_decimal(first_non_empty(form.get("renda_media_por_pescaria"), form.get("renda_por_pescaria"))),
            "petrechos_proprios": parse_bool(form.get("petrechos_proprios")),
            "petrechos_proprietario_se_nao": text_or_none(first_non_empty(form.get("petrechos_proprietario_se_nao"), form.get("petrechos_de_quem"))),
            "como_conserva_pescado": text_or_none(first_non_empty(form.get("como_conserva_pescado"), form.get("conservacao_pescado"))),
            "entrega_atravessador": parse_bool(first_non_empty(form.get("entrega_atravessador"))),
            "divida_com_atravessador": parse_bool(first_non_empty(form.get("divida_com_atravessador"), form.get("dividaAtravessador"))),
            "percepcao_pesca_passado": text_or_none(first_non_empty(form.get("percepcao_pesca_passado"), form.get("percepcao_pesca_hoje_vs_passado"))),
            "percepcao_tamanho_volume_capturado": text_or_none(first_non_empty(form.get("percepcao_tamanho_volume_capturado"), form.get("percepcao_tamanho_volume_pescado"))),
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
                    "nome_comum": text_or_none(item.get("nome_comum")),
                    "inicio_safra": item.get("inicio_safra") or None,
                    "fim_safra": item.get("fim_safra") or None,
                }
                for item in parsed
                if item.get("nome_comum")
            ]

        nomes = form.getlist("pescado_nome_comum[]") or form.getlist("pescado_nome_comum")
        inicios = form.getlist("pescado_inicio_safra[]") or form.getlist("pescado_inicio_safra")
        fins = form.getlist("pescado_fim_safra[]") or form.getlist("pescado_fim_safra")
        rows: list[dict[str, Any]] = []
        for index, nome_comum in enumerate(nomes):
            if not str(nome_comum).strip():
                continue
            rows.append(
                {
                    "pescador_id": pescador_id,
                    "nome_comum": text_or_none(nome_comum),
                    "inicio_safra": inicios[index] if index < len(inicios) and inicios[index] else None,
                    "fim_safra": fins[index] if index < len(fins) and fins[index] else None,
                }
            )
        return rows

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
                        "item_despesa": text_or_none(item.get("item_despesa")),
                        "tipo": text_or_none(item.get("tipo")),
                        "quantidade": parse_float(item.get("quantidade")),
                        "unidade": text_or_none(item.get("unidade")),
                        "custo_reais": parse_decimal(item.get("custo_reais")),
                        "outros": text_or_none(item.get("outros")),
                        "frequencia": normalize_enum_text(item.get("frequencia")),
                    }
                )
            return rows

        nomes = form.getlist("despesa_nome[]") or form.getlist("despesa_nome")
        tipos = form.getlist("despesa_tipo[]") or form.getlist("despesa_tipo")
        quantidades = form.getlist("despesa_quantidade[]") or form.getlist("despesa_quantidade")
        unidades = form.getlist("despesa_unidade[]") or form.getlist("despesa_unidade")
        custos = form.getlist("despesa_custo[]") or form.getlist("despesa_custo")
        outros = form.getlist("despesa_outros[]") or form.getlist("despesa_outros")
        frequencias = form.getlist("despesa_frequencia[]") or form.getlist("despesa_frequencia")

        rows = []
        for index, item_despesa in enumerate(nomes):
            if not str(item_despesa).strip():
                continue
            rows.append(
                {
                    "pescador_id": pescador_id,
                    "item_despesa": text_or_none(item_despesa),
                    "tipo": text_or_none(tipos[index] if index < len(tipos) else None),
                    "quantidade": parse_float(quantidades[index] if index < len(quantidades) else None),
                    "unidade": text_or_none(unidades[index] if index < len(unidades) else None),
                    "custo_reais": parse_decimal(custos[index] if index < len(custos) else None),
                    "outros": text_or_none(outros[index] if index < len(outros) else None),
                    "frequencia": normalize_enum_text(frequencias[index] if index < len(frequencias) else None),
                }
            )
        return rows

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

    def _normalize_categoria_pesca(self, value: Any):
        normalized = normalize_enum_text(value)
        if not normalized:
            return None

        aliases = {
            "artesanal": "pescador_artesanal",
            "pescador_artesanal": "pescador_artesanal",
            "industrial": "pescador_industrial",
            "pescador_industrial": "pescador_industrial",
            "armador": "armador",
        }
        return aliases.get(normalized, normalized)

    def _extract_id(self, response):
        data = getattr(response, "data", None)
        if isinstance(data, list) and data:
            row = data[0]
            if isinstance(row, dict):
                return row.get("id")
        return None
