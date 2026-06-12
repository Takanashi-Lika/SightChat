from __future__ import annotations

import os
from dataclasses import dataclass


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
