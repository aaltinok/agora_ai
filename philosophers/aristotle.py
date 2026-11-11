"""Aristoteles: sistematik, numaralı anlatım."""

from philosophers.base import Philosopher
from utils.textnorm import sentences, tr_lower


class Aristotle(Philosopher):
    def check_character(self, text: str) -> list[str]:
        problems = super().check_character(text)
        if len(sentences(text)) > 2 and "birincisi" not in tr_lower(text):
            problems.append("numaralı yapı yok")
        return problems
