"""Soru-cevap bankası: ayrıştırma, benzerlik eşleştirme, few-shot örnekleri.

Beklenen biçim:
    1. "Adalet nedir?"
    Sokrates: "Peki, bir öğretmen ..."
"""

from __future__ import annotations

import difflib
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from utils.textnorm import fold, stems

_Q = re.compile(r'^\s*\d+\.\s*["“](.+?)["”]\s*$')
_A = re.compile(r'^\s*([^\W\d_]+)\s*:\s*["“](.+)["”]\s*$')


@dataclass(frozen=True)
class Match:
    question: str
    answer: str
    score: float


def parse(text: str, known: set[str] | None = None) -> dict[str, list[tuple[str, str]]]:
    """{filozof: [(soru, cevap), ...]}. `known` verilirse yalnızca o adlar kabul edilir."""
    bank: dict[str, list[tuple[str, str]]] = {}
    question: str | None = None
    for line in text.splitlines():
        if m := _Q.match(line):
            question = m.group(1).strip()
        elif question and (m := _A.match(line)):
            name = m.group(1)
            if known is None or name in known:
                bank.setdefault(name, []).append((question, m.group(2).strip()))
            question = None
    return bank


def score(query: str, question: str) -> float:
    a, b = stems(query), stems(question)
    overlap = len(a & b) / min(len(a), len(b)) if a and b else 0.0
    ratio = difflib.SequenceMatcher(
        None, " ".join(fold(query).split()), " ".join(fold(question).split())
    ).ratio()
    return 0.6 * overlap + 0.4 * ratio


class QABank:
    def __init__(self, data: dict[str, list[tuple[str, str]]] | None = None) -> None:
        self._data = {k: tuple(v) for k, v in (data or {}).items()}

    @classmethod
    def from_text(cls, text: str, known: set[str] | None = None) -> QABank:
        return cls(parse(text, known))

    @classmethod
    def from_file(cls, path: Path | str, known: set[str] | None = None) -> QABank:
        p = Path(path)
        return cls.from_text(p.read_text(encoding="utf-8"), known) if p.is_file() else cls()

    @classmethod
    def from_files(cls, paths: Iterable[Path | str], known: set[str] | None = None) -> QABank:
        """Birden çok dosyayı birleştirir (sıra = öncelik: aynı skorda önceki kazanır)."""
        merged: dict[str, list[tuple[str, str]]] = {}
        for path in paths:
            bank = cls.from_file(path, known)
            for name in bank.philosophers:
                merged.setdefault(name, []).extend(bank.entries(name))
        return cls(merged)

    def __len__(self) -> int:
        return sum(len(v) for v in self._data.values())

    @property
    def philosophers(self) -> list[str]:
        return list(self._data)

    def entries(self, name: str) -> tuple[tuple[str, str], ...]:
        return self._data.get(name, ())

    def best_match(self, name: str, query: str, threshold: float = 0.6) -> Match | None:
        scored = [(score(query, q), q, a) for q, a in self.entries(name)]
        if not scored:
            return None
        s, q, a = max(scored, key=lambda c: c[0])
        return Match(q, a, s) if s >= threshold else None

    def shots(self, name: str, query: str = "", k: int = 3) -> list[tuple[str, str]]:
        """Few-shot: sorguya en yakın k örnek (sorgu yoksa ilk k)."""
        items = list(self.entries(name))
        if query:
            items.sort(key=lambda qa: -score(query, qa[0]))
        return items[:k]

    def duplicates(self) -> list[tuple[str, str]]:
        """Aynı filozofta tekrar eden sorular."""
        seen: set[tuple[str, str]] = set()
        dups: list[tuple[str, str]] = []
        for name, items in self._data.items():
            for q, _ in items:
                key = (name, fold(q))
                if key in seen:
                    dups.append((name, q))
                seen.add(key)
        return dups
