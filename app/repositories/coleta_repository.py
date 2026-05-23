from __future__ import annotations

from typing import Any


class ColetaRepository:
    def __init__(self, client: Any):
        self.client = client

    def create(self, payload: dict):
        return self.client.table("coletas").insert(payload).execute()

    def delete(self, coleta_id):
        return self.client.table("coletas").delete().eq("id", coleta_id).execute()
