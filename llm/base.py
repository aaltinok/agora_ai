"""Sağlayıcı arayüzü."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator, Sequence

from philosophers.base import Philosopher


class ProviderError(RuntimeError):
    """Sağlayıcı hatası. Mesaj asla URL, başlık veya anahtar içermez."""


class Provider(ABC):
    name: str = "provider"
    is_llm: bool = False

    @abstractmethod
    def stream(self, philosopher: Philosopher, history: Sequence[dict], mode: str) -> Iterator[str]:
        """Yanıtı parça parça üretir. `history` son mesajı kullanıcıya ait olmalıdır."""

    @abstractmethod
    def summarize(self, philosopher: Philosopher, history: Sequence[dict]) -> str:
        """Oturum özeti (Markdown)."""
