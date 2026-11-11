"""Sır (secret) yönetimi: okuma, maskeleme ve log'tan temizleme."""

from __future__ import annotations

import os
import re

_PATTERNS = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\b(?:sk|gsk|hf|ghp|xox[abp])[-_][A-Za-z0-9_\-]{8,}",
        r"\bBearer\s+[A-Za-z0-9._\-]{8,}",
        r"(?:api[_-]?key|token|secret|password)\s*[=:]\s*['\"]?[^\s'\"]{4,}",
    )
)
REDACTED = "[REDACTED]"


def redact(text: str) -> str:
    """Metindeki anahtar/token benzeri parçaları siler."""
    for pattern in _PATTERNS:
        text = pattern.sub(REDACTED, text)
    return text


def mask(value: str | None) -> str:
    """Gösterim için maskeler: uzun değerlerde yalnızca son 4 karakter."""
    if not value:
        return ""
    return f"***{value[-4:]}" if len(value) >= 16 else "****"


def get_secret(name: str, default: str = "") -> str:
    """Önce ortam değişkeni, sonra (varsa) Streamlit secrets."""
    value = os.environ.get(name)
    if value:
        return value
    try:
        import streamlit as st

        return str(st.secrets[name])
    except Exception:  # secrets dosyası yok / anahtar yok
        return default
