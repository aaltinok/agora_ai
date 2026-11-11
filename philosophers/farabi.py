"""Farabi: sistematik, kavram ayıran, akıl ve toplum odaklı."""

from philosophers.base import Philosopher
from utils.textnorm import tr_lower

_DOMAIN = ("akıl", "bilgi", "ilim", "saadet", "kavram", "öncül", "ayr", "düzen", "ilm")


class Farabi(Philosopher):
    def check_character(self, text: str) -> list[str]:
        problems = super().check_character(text)
        if not any(w in tr_lower(text) for w in _DOMAIN):
            problems.append("akıl/bilgi/düzen vurgusu yok")
        return problems
