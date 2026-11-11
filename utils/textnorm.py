"""Türkçe metin normalleştirme yardımcıları (bağımlılıksız, en alt katman)."""

from __future__ import annotations

import re

_FOLD = str.maketrans("ışçğöüâîû", "iscgouaiu")
_WORD = re.compile(r"[a-zçğıöşüâîû0-9]+")
_SENT = re.compile(r"(?<=[.!?…])\s+")
_QUOTES = re.compile(r"[\"'“”‘’«»`]")

STOPWORDS = frozenset(
    """
    ne nedir nasıl neden niçin niye kim kimdir hangi mi mı mu mü midir mıdır mudur müdür miyim
    mıyım musun misin bir bu şu o ve ile ama fakat ancak ya da veya için gibi kadar daha çok en
    de ki ben sen biz siz bana sana beni seni benim senin bizim sizin olur olmak olan olarak var
    yok her bütün hiç yapmalıyım yapmalı olmalı olmalıdır istiyorum düşünüyorum sence demek
    """.split()
)


def tr_lower(text: str) -> str:
    """Türkçe'ye duyarlı küçük harf (İ→i, I→ı)."""
    return text.replace("İ", "i").replace("I", "ı").lower()


def fold(text: str) -> str:
    """Küçük harf + aksan/Türkçe karakter sadeleştirme (eşleştirme için)."""
    return tr_lower(text).translate(_FOLD)


def tokens(text: str) -> list[str]:
    return _WORD.findall(tr_lower(text))


def keywords(text: str, n: int = 3) -> list[str]:
    """Metnin anlamlı kelimeleri (sırayı koruyarak, tekrarsız)."""
    seen: set[str] = set()
    out: list[str] = []
    for tok in tokens(text):
        if tok in STOPWORDS or len(tok) < 3 or tok in seen:
            continue
        seen.add(tok)
        out.append(tok)
    return out[:n]


def stems(text: str) -> set[str]:
    """Kaba kök kümesi: ilk 5 harf (ek farklarını tolere eder)."""
    return {fold(t)[:5] for t in tokens(text) if t not in STOPWORDS and len(t) > 1}


def sentences(text: str) -> list[str]:
    return [s for s in _SENT.split(text.strip()) if s]


def strip_quotes(text: str) -> str:
    return _QUOTES.sub("", text)


def truncate_words(text: str, limit: int) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.")
    return cut + "…"
