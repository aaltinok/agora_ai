"""Projede emoji kullanılmaz (arayüz, kod, doküman, senaryo)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EMOJI = re.compile("[\U0001f000-\U0001faff\u2300-\u23ff\u2600-\u27bf\u2b00-\u2bff\ufe0f\u200d]")
SKIP = {"vendor", ".git", "__pycache__", ".pytest_cache", ".ruff_cache", "fonts"}
TEXT = {".py", ".js", ".html", ".md", ".yaml", ".yml", ".json", ".toml", ".txt", ".cjs", ".example"}


def test_no_emoji_anywhere():
    offenders = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in TEXT and not SKIP & set(p.parts):
            found = EMOJI.findall(p.read_text(encoding="utf-8"))
            if found:
                offenders.append((str(p.relative_to(ROOT)), sorted(set(found))))
    assert not offenders, offenders
