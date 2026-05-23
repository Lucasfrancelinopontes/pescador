import json
import os
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

try:
    from supabase import Client, create_client as supabase_create_client  # type: ignore[import-not-found]
except ImportError:
    Client = Any  # type: ignore[assignment]
    supabase_create_client = None


load_dotenv()


@dataclass
class SupabaseSettings:
    url: str
    key: str


def get_settings() -> SupabaseSettings:
    return SupabaseSettings(
        url=os.getenv("SUPABASE_URL", "https://SEU_PROJETO_AQUI.supabase.co"),
        key=os.getenv("SUPABASE_KEY", "SUA_CHAVE_ANON_AQUI"),
    )


class _HTTPInsertBuilder:
    def __init__(self, client, table_name: str, payload: dict):
        self._client = client
        self._table_name = table_name
        self._payload = payload

    def execute(self):
        endpoint = f"{self._client.base_url}/rest/v1/{self._table_name}"
        headers = {
            "apikey": self._client.api_key,
            "authorization": f"Bearer {self._client.access_token or self._client.api_key}",
            "content-type": "application/json",
            "accept": "application/json",
            "prefer": "return=representation",
        }
        payload = json.dumps(self._payload, ensure_ascii=False).encode("utf-8")
        request_obj = Request(endpoint, data=payload, headers=headers, method="POST")
        try:
            with urlopen(request_obj, timeout=30) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw) if raw else []
                return SimpleNamespace(data=data)
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Erro ao inserir no Supabase: {detail}") from error
        except URLError as error:
            raise RuntimeError(f"Erro de conexão com o Supabase: {error}") from error


class _HTTPDeleteBuilder:
    def __init__(self, client, table_name: str):
        self._client = client
        self._table_name = table_name
        self._filters: list[tuple[str, str]] = []

    def eq(self, column: str, value):
        self._filters.append((column, str(value)))
        return self

    def execute(self):
        query_string = "&".join(f"{column}=eq.{value}" for column, value in self._filters)
        endpoint = f"{self._client.base_url}/rest/v1/{self._table_name}"
        if query_string:
            endpoint = f"{endpoint}?{query_string}"

        headers = {
            "apikey": self._client.api_key,
            "authorization": f"Bearer {self._client.access_token or self._client.api_key}",
            "accept": "application/json",
            "prefer": "return=minimal",
        }
        request_obj = Request(endpoint, headers=headers, method="DELETE")
        try:
            with urlopen(request_obj, timeout=30) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw) if raw else []
                return SimpleNamespace(data=data)
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Erro ao excluir no Supabase: {detail}") from error
        except URLError as error:
            raise RuntimeError(f"Erro de conexão com o Supabase: {error}") from error


class _HTTPTableClient:
    def __init__(self, client, table_name: str):
        self._client = client
        self._table_name = table_name

    def insert(self, payload: dict):
        return _HTTPInsertBuilder(self._client, self._table_name, payload)

    def delete(self):
        return _HTTPDeleteBuilder(self._client, self._table_name)


class _HTTPAuthClient:
    def __init__(self, client):
        self._client = client

    def sign_in_with_password(self, credentials: dict):
        endpoint = f"{self._client.base_url}/auth/v1/token?grant_type=password"
        headers = {
            "apikey": self._client.api_key,
            "content-type": "application/json",
            "accept": "application/json",
        }
        payload = json.dumps(credentials).encode("utf-8")
        request_obj = Request(endpoint, data=payload, headers=headers, method="POST")
        try:
            with urlopen(request_obj, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Falha no login: {detail}") from error
        except URLError as error:
            raise RuntimeError(f"Erro de conexão com o Supabase: {error}") from error

        user = SimpleNamespace(**data.get("user", {}))
        session_data = SimpleNamespace(
            access_token=data.get("access_token"),
            refresh_token=data.get("refresh_token"),
            token_type=data.get("token_type"),
            expires_in=data.get("expires_in"),
        )
        return SimpleNamespace(user=user, session=session_data)


class _HTTPClient:
    def __init__(self, base_url: str, api_key: str, access_token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.access_token = access_token
        self.auth = _HTTPAuthClient(self)

    def with_access_token(self, access_token: str | None):
        return _HTTPClient(self.base_url, self.api_key, access_token)

    def table(self, table_name: str):
        return _HTTPTableClient(self, table_name)


def create_supabase_client(access_token: str | None = None):
    settings = get_settings()
    # Futuras integrações com auditoria, service role e persistência avançada podem ser centralizadas aqui.
    if supabase_create_client is not None:
        client = supabase_create_client(settings.url, settings.key)
        if access_token and hasattr(client, "postgrest"):
            try:
                client.postgrest.auth(access_token)  # type: ignore[attr-defined]
            except Exception:
                pass
        return client
    return _HTTPClient(settings.url, settings.key, access_token)
