"""vr/src + three.js + diyalog JSON → tek dosyalık vr/dist/agora_vr.html (çevrimdışı çalışır)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VR = ROOT / "vr"
DIALOGUES = ROOT / "data" / "dialogues"
OUT = VR / "dist" / "agora_vr.html"
SOURCES = (
    "dialogue.js",
    "speech.js",
    "citizens.js",
    "props.js",
    "props2.js",
    "figures.js",
    "scenes.js",
    "app.js",
)


def _inline(js: str) -> str:
    """</script> dizisinin satır içi betiği erken kapatmasını engeller."""
    return js.replace("</", "<\\/")


PORTRAIT_OUT = VR / "dist" / "portraits.html"
PORTRAIT_SOURCES = ("citizens.js", "props.js", "figures.js", "portrait.js")


def build_portraits() -> Path:
    """Geliştirme aracı: portre üretimi için küçük bir sayfa (scripts/render_portraits.py kullanır)."""
    src = "\n".join((VR / "src" / name).read_text(encoding="utf-8") for name in PORTRAIT_SOURCES)
    three = (VR / "vendor" / "three.min.js").read_text(encoding="utf-8")
    html = f"<!doctype html><meta charset=utf-8><script>{_inline(three)}</script><script>{_inline(src)}</script>"
    PORTRAIT_OUT.write_text(html, encoding="utf-8")
    return PORTRAIT_OUT


def build() -> Path:
    data = {}
    for p in sorted(DIALOGUES.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        data[d["id"]] = d
    script = json.dumps(data, ensure_ascii=False)
    src = "\n".join((VR / "src" / name).read_text(encoding="utf-8") for name in SOURCES)
    html = (VR / "src" / "template.html").read_text(encoding="utf-8")
    html = (
        html.replace(
            "/*__THREE__*/", _inline((VR / "vendor" / "three.min.js").read_text(encoding="utf-8"))
        )
        .replace("/*__DIALOGUE_JSON__*/", _inline(script))
        .replace("/*__SRC__*/", _inline(src))
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    return OUT


if __name__ == "__main__":
    build_portraits()
    out = build()
    print(f"{out.relative_to(ROOT)}  ({out.stat().st_size / 1024:.0f} KB)")
