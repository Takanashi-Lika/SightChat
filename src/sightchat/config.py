from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(path: Path = Path(".env")) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text or text.startswith("#") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _get_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


_load_dotenv()


@dataclass(frozen=True)
class Settings:
    llm_provider: str = os.environ.get("SIGHTCHAT_LLM_PROVIDER", "mock")
    openai_base_url: str = os.environ.get("SIGHTCHAT_OPENAI_BASE_URL", "https://api.openai.com/v1")
    openai_api_key: str = os.environ.get("SIGHTCHAT_OPENAI_API_KEY", "")
    openai_model: str = os.environ.get("SIGHTCHAT_OPENAI_MODEL", "gpt-4o-mini")
    camera_index: int = _get_int("SIGHTCHAT_CAMERA_INDEX", 0)
    enable_cloud: bool = _get_bool("SIGHTCHAT_ENABLE_CLOUD", False)
    max_cloud_calls_per_minute: int = _get_int("SIGHTCHAT_MAX_CLOUD_CALLS_PER_MINUTE", 6)
    snapshot_max_width: int = _get_int("SIGHTCHAT_SNAPSHOT_MAX_WIDTH", 640)


settings = Settings()
