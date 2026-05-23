from __future__ import annotations

from typing import Any


class EmbarcacaoRepository:
    def __init__(self, client: Any):
        self.client = client

    def create(self, payload: dict):
        return self.client.table("embarcacoes").insert(payload).execute()

    def delete(self, embarcacao_id):
        return self.client.table("embarcacoes").delete().eq("id", embarcacao_id).execute()

    def create_propulsao(self, rows: list[dict]):
        if not rows:
            return None
        return self.client.table("embarcacao_propulsao").insert(rows).execute()
