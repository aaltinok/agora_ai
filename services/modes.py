"""API'siz motorun diyalog modları (şablon + sezgisel çözümleme)."""

from __future__ import annotations

from config.constants import DEFAULT_MODE
from philosophers.base import Philosopher
from services import argument
from utils.textnorm import keywords, strip_quotes, tr_lower, truncate_words

_TYPE_HINTS = (
    (("nedir", "ne demek", "tanım"), "tanım sorusu", "X derken tam olarak neyi kastediyoruz?"),
    (("neden", "niçin", "niye"), "gerekçe sorusu", "Bu iddiayı hangi neden destekliyor?"),
    (
        ("her zaman", "asla", "herkes", "mıdır", "midir"),
        "genel iddia sorusu",
        "İddianın yanlış olabileceği bir durum var mı?",
    ),
    (("nasıl",), "yöntem sorusu", "Bu sonuca hangi adımlarla ulaşılır?"),
)


def _claim(text: str) -> str:
    return truncate_words(strip_quotes(text).strip(" .!?…"), 120)


def analyze_question(text: str) -> str:
    low = tr_lower(text)
    kind, hint = "genel soru", "Bu düşüncenin doğru olması için neyi önceden kabul etmeliyiz?"
    for needles, k, h in _TYPE_HINTS:
        if any(n in low for n in needles):
            kind, hint = k, h
            break
    kws = ", ".join(keywords(text, 4)) or "—"
    return (
        f"**Soru türü:** {kind}\n\n**Anahtar kavramlar:** {kws}\n\n**Alt sorular:**\n"
        f"- {hint}\n- Kullandığım kavramları nasıl tanımlıyorum?\n"
        "- Aynı durumu başka nasıl açıklayabiliriz?"
    )


def aporia(p: Philosopher, text: str) -> str:
    claim = _claim(text)
    kw = (keywords(text, 1) or ["bu konu"])[0]
    return (
        f"Birlikte bir çıkmaza bakalım. İddian: “{claim}”.\n\n"
        "1. Bu iddiayı doğru kılan hangi önermeleri kabul ediyorsun?\n"
        "2. Aynı önermelerle çelişen makul bir durum düşünebilir misin?\n"
        "3. Hangi gizli varsayım bu çatışmayı doğuruyor?\n\n"
        f"Şimdilik çözemiyorsan “henüz bilmiyorum” diye kaydet ve şunu sonraki soruna çevir: "
        f"“{kw} hakkındaki hangi örnek iddiamı bozar?” ({p.name} tarzı)"
    )


def counterview(p: Philosopher, text: str) -> str:
    claim = _claim(text)
    concept = p.concepts[0]
    return (
        f"“{claim}” görüşüne karşı, savunucusunun da kabul edebileceği en güçlü üç itiraz ({p.name} tarzı):\n\n"
        "1. **Tanım itirazı:** Kullandığın temel kavram fazla geniş ya da dar olabilir.\n"
        "2. **Karşı örnek itirazı:** İddianın tam tersinin makul göründüğü bir durum var mı?\n"
        f"3. **Sonuç itirazı:** Öncüller sonucu zorunlu kılıyor mu? ({concept} açısından düşün.)\n\n"
        "Şimdi bu itirazı karikatürleştirmeden, en makul biçimiyle kendi cümlelerinle yaz ve ona yanıt ver."
    )


def apply(mode: str, p: Philosopher, text: str) -> str | None:
    """Normal dışı bir mod için yanıt; normal modda None."""
    if mode == DEFAULT_MODE:
        return None
    if mode == "Felsefi soru analizi":
        return analyze_question(text)
    if mode == "Argüman değerlendirme":
        return argument.render(argument.analyze(text))
    if mode == "Aporia modu":
        return aporia(p, text)
    if mode == "Karşıt görüş denemesi":
        return counterview(p, text)
    return None
