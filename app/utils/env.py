from __future__ import annotations

import os
from pathlib import Path


def load_env_file(env_path: str | Path | None = None) -> None:
    path = Path(env_path) if env_path is not None else Path(__file__).resolve().parents[2] / ".env"
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        name, value = line.split("=", 1)
        name = name.strip()
        value = value.strip().strip('"').strip("'")
        if name and name not in os.environ:
            os.environ[name] = value
