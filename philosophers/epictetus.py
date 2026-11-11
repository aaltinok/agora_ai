"""Epiktetos: kontrol ayrımı, sakin öğreticilik."""

from philosophers.base import Philosopher
from utils.textnorm import tr_lower

_CONTROL = ("bağlı", "irade", "yargı")


class Epictetus(Philosopher):
    def check_character(self, text: str) -> list[str]:
        problems = super().check_character(text)
        if not any(w in tr_lower(text) for w in _CONTROL):
            problems.append("kontrol ayrımı vurgusu yok")
        return problems
