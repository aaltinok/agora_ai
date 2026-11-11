"""Oturum durumu ve gezinme."""

from __future__ import annotations

from collections.abc import MutableMapping

from config.constants import DEFAULT_MODE
from config.settings import Settings
from safety.ratelimit import SlidingWindowLimiter

# (etiket, Material simgesi): ekran görüntüsündeki sol menü
NAV = [
    ("Ana Sayfa", "home"),
    ("Sohbet", "chat_bubble"),
    ("Filozoflar", "groups"),
    ("Karşılaştır", "compare_arrows"),
    ("Oturumlar", "description"),
    ("Sesli Diyalog", "mic"),
    ("Yüz Yüze", "forum"),
    ("3B Agora", "view_in_ar"),
    ("Soru Bankası", "menu_book"),
    ("İleri Düzey", "tune"),
    ("Ayarlar", "settings"),
]
PAGES = [label for label, _ in NAV]


def init_state(state: MutableMapping, settings: Settings, default_philosopher: str) -> None:
    defaults = {
        "page": PAGES[0],
        "philosopher": default_philosopher,
        "chats": {},
        "notes": {},
        "summaries": {},
        "dialogue": {},
        "mode": DEFAULT_MODE,
        "pending": False,
        "force_rule": False,
        "theme": "Koyu",
        "voice_replies": True,
        "reminders": False,
        "adv": "Felsefi Soru Analizörü",
        "voice_ts": 0,
        "voice_base": {},
    }
    for key, value in defaults.items():
        state.setdefault(key, value)
    if "limiter" not in state:
        state["limiter"] = SlidingWindowLimiter(settings.rate_limit_per_min, 60.0)
