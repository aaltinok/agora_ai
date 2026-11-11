"""Kriz ifadesi tespiti. Eşleşirse persona yerine sakin bir destek mesajı gösterilir.

Bilinçli olarak dar tutulmuştur: "Ölümden korkuyorum" gibi felsefi/duygusal sorular
eşleşmez; açık niyet veya plan bildiren ifadeler eşleşir.
"""

from __future__ import annotations

import re

from utils.textnorm import fold

_PATTERNS = tuple(
    re.compile(p)
    for p in (
        r"\bintihar",
        r"\bkendimi (?:oldur|asa|bicakla|atacag|yakacag|bitir)",
        r"\bkendime (?:zarar|kiy)",
        r"\bcanima kiy",
        r"\byasamak istemiyorum",
        r"\bolmek istiyorum",
        r"\bhayatima son",
        r"\bolup gitmek istiyorum",
    )
)

CRISIS_RESPONSE = (
    "Yazdıklarını ciddiye alıyorum ve felsefe tartışmasını şimdilik bir kenara bırakıyorum. "
    "Kendine zarar verme düşüncen varsa ya da acil bir tehlikedeysen lütfen hemen 112 Acil Çağrı "
    "Merkezi'ni ara. Güvendiğin birine (aile üyesi, arkadaş, öğretmen) şu an durumu söyle ve "
    "yalnız kalmamaya çalış. Bir sağlık kuruluşuna ya da ruh sağlığı uzmanına başvurmak da "
    "önemli bir adımdır. Agora AI bir kriz hizmeti değildir; seni destekleyebilecek insanlara "
    "ulaşman çok değerli."
)


def detect(text: str) -> bool:
    folded = fold(text)
    return any(p.search(folded) for p in _PATTERNS)
