"""Filozof kayıt defteri: YAML'dan yükler, uygun sınıfla örnekler."""

from __future__ import annotations

from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path
from typing import Any

from config.loader import load_philosophers
from philosophers.aristotle import Aristotle
from philosophers.base import Philosopher
from philosophers.epictetus import Epictetus
from philosophers.farabi import Farabi
from philosophers.plato import Plato
from philosophers.socrates import Socrates

# Özel mantığı olan filozoflar; listede olmayanlar taban sınıfla çalışır.
_CLASSES: dict[str, type[Philosopher]] = {
    "sokrates": Socrates,
    "platon": Plato,
    "aristoteles": Aristotle,
    "epiktetos": Epictetus,
    "farabi": Farabi,
}


class Registry:
    def __init__(self, configs: dict[str, dict[str, Any]]) -> None:
        self._by_name: dict[str, Philosopher] = {}
        for key, cfg in configs.items():
            philosopher = _CLASSES.get(key, Philosopher).from_config(key, cfg)
            self._by_name[philosopher.name] = philosopher

    def __getitem__(self, name: str) -> Philosopher:
        return self._by_name[name]

    def __iter__(self) -> Iterator[Philosopher]:
        return iter(self._by_name.values())

    def __len__(self) -> int:
        return len(self._by_name)

    def __contains__(self, name: object) -> bool:
        return name in self._by_name

    @property
    def names(self) -> list[str]:
        return list(self._by_name)


@lru_cache(maxsize=4)
def _cached(path: str | None) -> Registry:
    return Registry(load_philosophers(path) if path else load_philosophers())


def get_registry(path: Path | str | None = None) -> Registry:
    return _cached(str(path) if path else None)
