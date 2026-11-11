"""Ortam tabanlı, doğrulanmış ayarlar. Sırlar repr/log çıktısına girmez."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

from config.paths import ROOT
from utils.secrets import get_secret, mask

ENGINES = ("rule", "llm")
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


class SettingsError(ValueError):
    """Geçersiz yapılandırma."""


@dataclass(frozen=True)
class Settings:
    engine: str = "rule"
    llm_base_url: str = "http://localhost:11434/v1"
    llm_model: str = "qwen2.5:7b"
    llm_api_key: str = field(default="", repr=False)
    llm_timeout_s: int = 60
    max_input_chars: int = 800
    rate_limit_per_min: int = 12
    session_ttl_minutes: int = 60
    max_history_messages: int = 40
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        if self.engine not in ENGINES:
            raise SettingsError(f"AGORA_ENGINE şunlardan biri olmalı: {', '.join(ENGINES)}")
        if self.log_level.upper() not in LOG_LEVELS:
            raise SettingsError("AGORA_LOG_LEVEL geçersiz.")
        for name, lo, hi in (
            ("llm_timeout_s", 1, 600),
            ("max_input_chars", 20, 5000),
            ("rate_limit_per_min", 1, 600),
            ("session_ttl_minutes", 1, 1440),
            ("max_history_messages", 2, 200),
        ):
            value = getattr(self, name)
            if not isinstance(value, int) or not lo <= value <= hi:
                raise SettingsError(f"{name} {lo}-{hi} aralığında bir tam sayı olmalı.")
        self._validate_url()

    def _validate_url(self) -> None:
        url = urlparse(self.llm_base_url)
        if url.scheme not in ("http", "https") or not url.hostname:
            raise SettingsError("AGORA_LLM_BASE_URL http(s) adresi olmalı.")
        if url.username or url.password:
            raise SettingsError("URL içine kullanıcı/parola yazmayın; AGORA_LLM_API_KEY kullanın.")
        if url.scheme == "http" and url.hostname not in LOCAL_HOSTS:
            raise SettingsError("Uzak sunucular için https zorunludur (http yalnızca localhost).")

    @property
    def uses_llm(self) -> bool:
        return self.engine == "llm"

    def public(self) -> dict[str, object]:
        """Arayüzde gösterilebilir, sırsız görünüm."""
        data = {f.name: getattr(self, f.name) for f in fields(self)}
        data["llm_api_key"] = mask(self.llm_api_key) or "(yok)"
        return data


def _read_dotenv(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        out[key.strip()] = value.strip().strip("'\"")
    return out


def _int(env: Mapping[str, str], key: str, default: int) -> int:
    raw = env.get(key, "")
    if raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        raise SettingsError(f"{key} tam sayı olmalı.") from None


def load_settings(env: Mapping[str, str] | None = None, dotenv: Path | None = None) -> Settings:
    """`env` verilirse yalnızca onu kullanır (test); yoksa .env + ortam + secrets."""
    if env is None:
        merged = {**_read_dotenv(dotenv or ROOT / ".env"), **os.environ}
        merged.setdefault("AGORA_LLM_API_KEY", get_secret("AGORA_LLM_API_KEY"))
        env = merged
    d = Settings()
    return Settings(
        engine=env.get("AGORA_ENGINE", d.engine).strip().lower(),
        llm_base_url=env.get("AGORA_LLM_BASE_URL", d.llm_base_url).strip(),
        llm_model=env.get("AGORA_LLM_MODEL", d.llm_model).strip(),
        llm_api_key=env.get("AGORA_LLM_API_KEY", ""),
        llm_timeout_s=_int(env, "AGORA_LLM_TIMEOUT", d.llm_timeout_s),
        max_input_chars=_int(env, "AGORA_MAX_INPUT_CHARS", d.max_input_chars),
        rate_limit_per_min=_int(env, "AGORA_RATE_LIMIT_PER_MIN", d.rate_limit_per_min),
        session_ttl_minutes=_int(env, "AGORA_SESSION_TTL_MIN", d.session_ttl_minutes),
        max_history_messages=_int(env, "AGORA_MAX_HISTORY", d.max_history_messages),
        log_level=env.get("AGORA_LOG_LEVEL", d.log_level).strip().upper(),
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()
