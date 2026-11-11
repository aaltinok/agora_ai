"""Sağlayıcı seçimi ve otomatik geri düşüş (fallback)."""

from __future__ import annotations

import logging
from collections.abc import Iterator, Sequence

from config.settings import Settings
from llm.base import Provider, ProviderError
from llm.openai_compat import OpenAICompatProvider
from llm.rule_based import RuleBasedProvider
from philosophers.base import Philosopher
from services.qa_bank import QABank

log = logging.getLogger("agora.llm")
FALLBACK_NOTICE = "Uyarı: Yerel model yanıt vermedi; kural tabanlı moda geçildi.\n\n"


class FallbackProvider(Provider):
    """Birincil sağlayıcı hata verirse kural tabanlı motora düşer."""

    def __init__(self, primary: Provider, fallback: Provider) -> None:
        self._primary, self._fallback = primary, fallback
        self.name, self.is_llm = primary.name, primary.is_llm

    @property
    def primary(self) -> Provider:
        return self._primary

    def stream(self, philosopher: Philosopher, history: Sequence[dict], mode: str) -> Iterator[str]:
        started = False
        try:
            for chunk in self._primary.stream(philosopher, history, mode):
                started = True
                yield chunk
            return
        except ProviderError:
            log.warning("primary_provider_failed started=%s", started)
            if started:
                yield "\n\nUyarı: Bağlantı yarıda kesildi."
                return
        yield FALLBACK_NOTICE
        yield from self._fallback.stream(philosopher, history, mode)

    def summarize(self, philosopher: Philosopher, history: Sequence[dict]) -> str:
        return self._primary.summarize(philosopher, history)


def build_provider(settings: Settings, bank: QABank) -> Provider:
    rule = RuleBasedProvider(bank)
    if not settings.uses_llm:
        return rule
    return FallbackProvider(OpenAICompatProvider(settings, bank), rule)
