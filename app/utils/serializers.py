from __future__ import annotations

import json
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def audit_fields(user_id: str | None) -> dict[str, Any]:
    now = utc_now_iso()
    return {
        "created_at": now,
        "updated_at": now,
        "created_by": user_id,
    }


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "on", "sim", "s"}


def parse_int(value: Any):
    text = str(value).strip() if value is not None else ""
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def parse_float(value: Any):
    text = str(value).strip() if value is not None else ""
    if not text:
        return None
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


def parse_decimal(value: Any):
    text = str(value).strip() if value is not None else ""
    if not text:
        return None
    try:
        return Decimal(text.replace(",", "."))
    except Exception:
        return None


def parse_date(value: Any):
    text = str(value).strip() if value is not None else ""
    if not text:
        return None
    try:
        return date.fromisoformat(text).isoformat()
    except ValueError:
        return None


def parse_json(value: Any, default: Any):
    if value is None or value == "":
        return default
    if isinstance(value, (list, dict)):
        return value
    try:
        return json.loads(value)
    except Exception:
        return default


def ensure_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        parsed = parse_json(value, [])
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]
        return [item.strip() for item in value.split(";") if item.strip()]
    return [str(value).strip()]


def first_non_empty(*values: Any, default: Any = None):
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        return value
    return default
