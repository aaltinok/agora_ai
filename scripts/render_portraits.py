"""Filozof portrelerini ve ana sayfa görselini 3B modellerden üretir (Playwright + Chromium gerekir).

    python scripts/render_portraits.py
Çıktı: ui/assets/portraits/<id>.png ve ui/assets/hero.jpg
"""

from __future__ import annotations

import base64
from pathlib import Path

from playwright.sync_api import sync_playwright

from scripts import build_vr

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ui" / "assets"
ACCENTS = {
    "sokrates": "#3FA66B",
    "platon": "#4F8CFF",
    "aristoteles": "#E08A3C",
    "epiktetos": "#D6B25A",
    "farabi": "#9B6BD6",
}
GL = [
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
    "--ignore-gpu-blocklist",
]


def main() -> None:
    build_vr.build_portraits()
    build_vr.build()
    (OUT / "portraits").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=GL)
        page = b.new_page()
        page.goto(build_vr.PORTRAIT_OUT.resolve().as_uri())
        for pid, accent in ACCENTS.items():
            url = page.evaluate(f"renderPortrait('{pid}', '{accent}', 512)")
            (OUT / "portraits" / f"{pid}.png").write_bytes(base64.b64decode(url.split(",", 1)[1]))
        hero = b.new_page(viewport={"width": 1600, "height": 520})
        hero.goto(build_vr.OUT.resolve().as_uri())
        hero.wait_for_selector("#options button")
        hero.evaluate("document.getElementById('hud').style.display='none'; AGORA.look(0.0, -0.02)")
        hero.wait_for_timeout(2500)
        hero.screenshot(path=str(OUT / "hero.jpg"), type="jpeg", quality=82)
        b.close()
    print("portreler ve hero.jpg üretildi")


if __name__ == "__main__":
    main()
