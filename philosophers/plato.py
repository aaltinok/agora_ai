"""Platon: alegori ve idea vurgusu."""

from philosophers.base import Philosopher
from utils.textnorm import tr_lower

_IMAGERY = ("idea", "gölge", "mağara", "ölçüt", "hikâye", "geometri", "ruh")


class Plato(Philosopher):
    def check_character(self, text: str) -> list[str]:
        problems = super().check_character(text)
        if not any(w in tr_lower(text) for w in _IMAGERY):
            problems.append("alegori/idea göndermesi yok")
        return problems
