"""Girdi hattı: temizle → kriz → hız sınırı → injection → (devam | hazır yanıt)."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from safety import crisis
from safety.ratelimit import SlidingWindowLimiter
from safety.sanitize import sanitize

log = logging.getLogger("agora.pipeline")

INJECTION_REPLY = (
    "Bu mesaj sistem kurallarını değiştirmeye çalışıyor gibi görünüyor; bunu uygulamıyorum. "
    "Felsefi sorunu ya da iddianı yeniden yazarsan birlikte düşünebiliriz."
)


@dataclass(frozen=True)
class Decision:
    action: str  # "proceed" | "reply"
    clean: str = ""
    reply: str = ""
    reason: str = ""  # "", "empty", "crisis", "rate_limited", "injection"
    notice: str = ""


def pre_process(raw: str, *, max_chars: int, limiter: SlidingWindowLimiter) -> Decision:
    s = sanitize(raw, max_chars)
    if not s.text:
        return Decision("reply", "", "Lütfen bir soru ya da iddia yaz.", "empty")
    if crisis.detect(s.text):  # kriz mesajı hız sınırına takılmaz
        log.info("decision=crisis")
        return Decision("reply", s.text, crisis.CRISIS_RESPONSE, "crisis")
    if not limiter.allow():
        wait = limiter.retry_after()
        log.info("decision=rate_limited")
        return Decision(
            "reply", s.text, f"Çok hızlı yazıyorsun; {wait} sn sonra tekrar dene.", "rate_limited"
        )
    if s.injection:
        log.info("decision=injection")
        return Decision("reply", s.text, INJECTION_REPLY, "injection")
    notice = f"Mesaj {max_chars} karaktere kısaltıldı." if s.truncated else ""
    return Decision("proceed", s.text, notice=notice)
