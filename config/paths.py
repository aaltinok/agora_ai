"""Proje yolları ve güvenli yol birleştirme."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
TEXTS_DIR = DATA_DIR / "texts"
PHILOSOPHERS_YAML = CONFIG_DIR / "philosophers.yaml"
QA_BANK_PATH = TEXTS_DIR / "qa_bank.md"


def safe_join(base: Path, *parts: str) -> Path:
    """`base` dışına çıkan (../) yolları reddeder."""
    base = base.resolve()
    target = base.joinpath(*parts).resolve()
    if base != target and base not in target.parents:
        raise ValueError("Yol, izin verilen klasörün dışına çıkıyor.")
    return target


QA_VR_PATH = TEXTS_DIR / "qa_sokrates_vr.md"
DIALOGUE_DIR = DATA_DIR / "dialogues"
VR_DIST = ROOT / "vr" / "dist" / "agora_vr.html"
