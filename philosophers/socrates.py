"""Sokrates (VR taslağı kuralları): önce açık cevap, sonra karşı soru; hüküm vermez."""

from philosophers.base import Philosopher
from utils.textnorm import tr_lower

# Öğrencinin cevabını hemen doğru/yanlış diye değerlendirmemeli.
_VERDICTS = (
    "doğru söyledin",
    "yanlış söyledin",
    "yanlışsın",
    "haklısın",
    "tebrikler",
    "kesinlikle yanlış",
)


class Socrates(Philosopher):
    def check_character(self, text: str) -> list[str]:
        problems = super().check_character(text)
        if not text.rstrip().endswith("?"):
            problems.append("karşı soruyla bitmeli")
        low = tr_lower(text)
        problems += [f"hemen değerlendiriyor: {v}" for v in _VERDICTS if v in low]
        return problems
