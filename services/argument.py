"""Argüman çözümleme: iddia / öncül ayrımı ve sezgisel zayıflık işaretleri."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from utils.textnorm import tr_lower

_PREMISE_AFTER = re.compile(r"\b(çünkü|zira|madem(?:ki)?)\b")
_PREMISE_BEFORE = re.compile(r"\b(bu yüzden|bu nedenle|dolayısıyla|o hâlde|öyleyse|sonuç olarak)\b")
_ABSOLUTES = ("herkes", "hiç kimse", "her zaman", "asla", "hiçbir", "kesinlikle", "bütün", "tüm ")
_EXAMPLE_MARKERS = ("örneğin", "mesela", "misal")
QUESTIONS = (
    "Öncüller doğru mu, yoksa yalnızca varsayılmış mı?",
    "Sonuç, öncüllerden gerçekten çıkıyor mu; yoksa onlardan daha güçlü mü?",
    "İddianın yanlış olabileceği en güçlü karşı örnek nedir?",
)


@dataclass(frozen=True)
class ArgumentAnalysis:
    claim: str
    premises: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    questions: tuple[str, ...] = QUESTIONS


def analyze(text: str) -> ArgumentAnalysis:
    text = " ".join(text.split())
    low = tr_lower(text)  # İ→i dönüşümü uzunluğu korur; indeksler orijinalle eşleşir
    claim, premises = text, []
    if m := _PREMISE_AFTER.search(low):
        claim, premises = text[: m.start()], [text[m.end() :]]
    elif m := _PREMISE_BEFORE.search(low):
        premises, claim = [text[: m.start()]], text[m.end() :]
    claim = claim.strip(" ,;:.")
    premises = [p.strip(" ,;:.") for p in premises if p.strip(" ,;:.")]

    issues: list[str] = []
    if not premises:
        issues.append("Gerekçe belirtilmemiş: iddia varsayılmış olabilir.")
    elif len(premises) == 1:
        issues.append("Tek öncül var: yanlışsa sonuç çöker; ikinci bir destek arayın.")
    issues += [
        f"Mutlak ifade (“{w.strip()}”): tek bir karşı örnek iddiayı çürütebilir."
        for w in _ABSOLUTES
        if w in low
    ][:2]
    if any(w in low for w in _EXAMPLE_MARKERS):
        issues.append("Örnek, kanıt yerine kullanılıyor olabilir.")
    return ArgumentAnalysis(claim, premises, issues)


def render(a: ArgumentAnalysis) -> str:
    lines = [f"**İddia:** {a.claim or '—'}", "", "**Öncüller:**"]
    lines += [f"- {p}" for p in a.premises] or ["- (belirtilmemiş)"]
    lines += ["", "**Olası sorunlar:**", *[f"- {i}" for i in a.issues], "", "**Kendinize sorun:**"]
    lines += [f"- {q}" for q in a.questions]
    return "\n".join(lines)
