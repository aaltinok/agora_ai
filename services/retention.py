"""Veri saklama ilkesi: yalnızca bellek, TTL ile silme, tek tıkla temizleme."""

from __future__ import annotations

import time
from collections.abc import MutableMapping, Sequence

DATA_KEYS = ("chats", "notes", "summaries", "dialogue")
EXCLUDED_KINDS = frozenset({"safety", "system"})


def touch(state: MutableMapping, now: float | None = None) -> None:
    state["last_activity"] = time.time() if now is None else now


def expired(state: MutableMapping, ttl_s: float, now: float | None = None) -> bool:
    last = state.get("last_activity")
    return last is not None and (time.time() if now is None else now) - last > ttl_s


def wipe(state: MutableMapping) -> None:
    for key in DATA_KEYS:
        state[key] = {}
    state["pending"] = False


def purge_if_expired(state: MutableMapping, ttl_s: float, now: float | None = None) -> bool:
    if expired(state, ttl_s, now):
        wipe(state)
        return True
    return False


def conversation(history: Sequence[dict]) -> list[dict]:
    """Dışa aktarma / özet / model için: güvenlik ve sistem mesajları hariç."""
    return [m for m in history if m.get("kind") not in EXCLUDED_KINDS]


def llm_messages(history: Sequence[dict], max_messages: int) -> list[dict]:
    """Modele giden {role, content} listesi; kırpılmış ve 'user' ile başlayan."""
    msgs = [{"role": m["role"], "content": m["content"]} for m in conversation(history)]
    msgs = msgs[-max_messages:]
    while msgs and msgs[0]["role"] != "user":
        msgs.pop(0)
    return msgs
