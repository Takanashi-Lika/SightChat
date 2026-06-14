import os
from pathlib import Path

from sightchat.config import _load_dotenv


def test_load_dotenv_reads_local_values(tmp_path, monkeypatch) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text("SIGHTCHAT_LLM_PROVIDER=deepseek\nSIGHTCHAT_OPENAI_MODEL=deepseek-chat\n", encoding="utf-8")
    monkeypatch.delenv("SIGHTCHAT_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("SIGHTCHAT_OPENAI_MODEL", raising=False)

    _load_dotenv(Path(env_path))

    assert os.environ["SIGHTCHAT_LLM_PROVIDER"] == "deepseek"
    assert os.environ["SIGHTCHAT_OPENAI_MODEL"] == "deepseek-chat"


def test_load_dotenv_does_not_override_existing_env(tmp_path, monkeypatch) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text("SIGHTCHAT_LLM_PROVIDER=deepseek\n", encoding="utf-8")
    monkeypatch.setenv("SIGHTCHAT_LLM_PROVIDER", "mock")

    _load_dotenv(Path(env_path))

    assert os.environ["SIGHTCHAT_LLM_PROVIDER"] == "mock"
