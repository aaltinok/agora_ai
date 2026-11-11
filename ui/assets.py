"""Görsel varlıklar: portreler ve ana sayfa görseli (data URI olarak HTML'e gömülür)."""

from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"


@lru_cache(maxsize=32)
def data_uri(rel: str) -> str:
    path = ASSETS / rel
    if not path.is_file():
        return ""
    mime = "image/jpeg" if path.suffix == ".jpg" else "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def portrait(key: str) -> str:
    return data_uri(f"portraits/{key}.png")


def hero() -> str:
    return data_uri("hero.jpg")
