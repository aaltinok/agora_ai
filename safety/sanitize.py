"""Kullanıcı girdisini temizleme ve prompt-injection sezgisi."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from utils.textnorm import fold

_CONTROL = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]"
)
_INJECTION = tuple(
    re.compile(p)
    for p in (
        r"onceki (?:tum )?(?:talimat|komut|kural|yonerge)",
        r"(?:talimat|kural|komut|yonerge)\w* (?:yoksay|unut|gecersiz)",
        r"sistem (?:istem|mesaj|prompt)",
        r"system prompt",
        r"ignore (?:all |any )?(?:previous|prior|above)",
        r"jailbreak",
        r"developer mode",
    )
)


@dataclass(frozen=True)
class Sanitized:
    text: str
    truncated: bool = False
    injection: bool = False


def sanitize(raw: str, max_chars: int) -> Sanitized:
    text = unicodedata.normalize("NFC", raw or "")
    text = _CONTROL.sub("", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    truncated = len(text) > max_chars
    if truncated:
        text = text[:max_chars].rstrip()
    folded = fold(text)
    return Sanitized(text, truncated, any(p.search(folded) for p in _INJECTION))
