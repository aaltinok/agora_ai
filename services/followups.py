"""VR taslağındaki "öğrencinin seçebileceği sorular" ve "bilmiyorum" tespiti.

Yanıt şablonları taslak olarak yazılmıştır (belgede bu soruların cevabı yoktur); öğretmen gözden geçirmelidir.
"""

from __future__ import annotations

from utils.textnorm import fold, sentences, tokens, truncate_words

STUDENT_QUESTIONS = (
    "Bunu biraz daha açıklar mısın?",
    "Düşünceni bir örnekle anlatabilir misin?",
    "Neden böyle düşünüyorsun?",
    "Bu düşüncene karşı çıkan birine ne söylerdin?",
    "Söylediklerinin günümüzde de geçerli olduğunu düşünüyor musun?",
    "Bu konuda başka bir bakış açısı olabilir mi?",
    "Peki, sen bana ne sormak istersin?",
)
_REPLIES = (
    "Elbette. Şunu söylemiştim: “{last}” Bunun hangi kısmı sana belirsiz geldi?",
    "Bir örnek üzerinden düşünelim: günlük hayatından bunu açıklayan bir durum seç. Sence söylediğim hangi durumda geçerli olmaz?",
    "Çünkü bir düşünceyi gerekçesini sormadan kabul etmek istemem. Sen bu konudaki kendi düşüncenin gerekçesini nasıl açıklarsın?",
    "Ona önce neden karşı çıktığını sorardım ve gerekçesini dinlerdim. Sence onun en güçlü itirazı ne olurdu?",
    "Araçlar değişse de insanın nasıl yaşaması gerektiği sorusu önemini koruyor. Sen günümüzden hangi örneği verirdin?",
    "Elbette olabilir; aynı soruya başka biri başka bir çıkarla ya da deneyimle bakabilir. Sence karşı bir görüş nasıl savunulurdu?",
    "Seni dinliyorum, genç dostum. Ben her şeyi bilmediğimi bilirim, birlikte araştırırız. Aklındaki soru nedir?",
)
_INDEX = {fold(q): i for i, q in enumerate(STUDENT_QUESTIONS)}
_UNCERTAIN = ("bilmiyorum", "bilemiyorum", "emin degilim", "kararsizim", "fikrim yok")


def is_uncertain(text: str) -> bool:
    """Kısa ve belirsizlik bildiren mesaj mı ("Bilmiyorum" gibi)?"""
    return len(tokens(text)) <= 8 and any(u in fold(text) for u in _UNCERTAIN)


def reply_for(text: str, last_assistant: str = "") -> str | None:
    """Hazır öğrenci sorusuna yanıt; eşleşmezse None."""
    i = _INDEX.get(fold(text).strip())
    if i is None:
        return None
    last = (
        truncate_words(" ".join(sentences(last_assistant)[:2]), 160) or "Henüz bir şey söylemedim"
    )
    return _REPLIES[i].format(last=last)
