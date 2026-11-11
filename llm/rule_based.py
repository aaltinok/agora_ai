"""API'siz motor: soru bankası + filozof şablonları + mod çözümleyicileri."""

from __future__ import annotations

import time
from collections.abc import Iterator, Sequence

from config.constants import DEFAULT_MODE
from llm.base import Provider
from philosophers.base import Philosopher
from services import followups, modes, summary
from services.qa_bank import QABank
from utils.textnorm import keywords


class RuleBasedProvider(Provider):
    name = "Kural tabanlı (API'siz, çevrimdışı)"
    is_llm = False

    def __init__(self, bank: QABank, delay: float = 0.012) -> None:
        self._bank, self._delay = bank, delay

    def respond(self, p: Philosopher, history: Sequence[dict], mode: str = DEFAULT_MODE) -> str:
        text = history[-1]["content"]
        said = [m["content"] for m in history if m["role"] == "assistant"]
        avoid, turn, kws = set(said), len(said), keywords(text)
        if (out := modes.apply(mode, p, text)) is not None:
            return out
        if (out := followups.reply_for(text, said[-1] if said else "")) is not None:
            return out
        if followups.is_uncertain(text):
            return p.compose_uncertain(kws, turn, avoid)
        match = self._bank.best_match(p.name, text)
        if match and match.answer not in avoid:  # aynı cevap/karşı soru tekrarlanmaz
            return match.answer
        if not kws and turn == 0:
            return p.fallback
        return p.compose(kws, text, turn, avoid)

    def stream(
        self, philosopher: Philosopher, history: Sequence[dict], mode: str = DEFAULT_MODE
    ) -> Iterator[str]:
        for token in self.respond(philosopher, history, mode).split(" "):
            yield token + " "
            if self._delay:
                time.sleep(self._delay)

    def summarize(self, philosopher: Philosopher, history: Sequence[dict]) -> str:
        return summary.summarize(history, philosopher.name)
