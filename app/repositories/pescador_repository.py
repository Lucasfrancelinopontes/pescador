from __future__ import annotations

from typing import Any


class PescadorRepository:
    def __init__(self, client: Any):
        self.client = client

    def create(self, payload: dict):
        return self.client.table("pescadores").insert(payload).execute()

    def delete(self, pescador_id):
        return self.client.table("pescadores").delete().eq("id", pescador_id).execute()

    def create_relacao_trabalho(self, rows: list[dict]):
        if not rows:
            return None
        return self.client.table("tipo_relacao_trabalho").insert(rows).execute()

    def create_pescados_safra(self, rows: list[dict]):
        if not rows:
            return None
        return self.client.table("pescados_safra").insert(rows).execute()

    def create_despesas_atividade(self, rows: list[dict]):
        if not rows:
            return None
        return self.client.table("despesas_atividade").insert(rows).execute()
