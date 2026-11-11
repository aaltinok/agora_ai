"""Çıkarımsal (extractive) oturum özeti — model gerektirmez."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

from utils.textnorm import keywords, sentences, truncate_words


def summarize(history: Sequence[dict], name: str) -> str:
    users = [m["content"] for m in history if m["role"] == "user"]
    bots = [m["content"] for m in history if m["role"] == "assistant"]
    if not users:
        return "Henüz özetlenecek bir diyalog yok."
    freq = Counter(k for u in users for k in keywords(u, 5))
    topics = ", ".join(k for k, _ in freq.most_common(3)) or "—"
    open_q = next(
        (s for b in reversed(bots) for s in reversed(sentences(b)) if s.endswith("?")), "—"
    )
    return (
        f"**Filozof:** {name}\n\n**Ana kavramlar:** {topics}\n\n"
        f"**İlk söz:** “{truncate_words(users[0], 100)}”\n\n"
        f"**Son söz:** “{truncate_words(users[-1], 100)}”\n\n"
        f"**Açık kalan soru:** {truncate_words(open_q, 160)}\n\n"
        f"**Tur sayısı:** {len(users)}"
    )
