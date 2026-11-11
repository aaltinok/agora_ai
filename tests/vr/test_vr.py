"""VR istemcisi testleri: JS/Python parite, Türkçe sesli komut eşleştirme, derleme, tarayıcı duman testi."""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from config.paths import DIALOGUE_DIR
from scripts import build_vr
from services import dialogue as d

ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
needs_node = pytest.mark.skipif(NODE is None, reason="node yok")
SCRIPTS = d.load_scripts(DIALOGUE_DIR)


def _js(sid, *args):
    out = subprocess.run(
        [
            NODE,
            str(ROOT / "tests/js/dialogue_runner.cjs"),
            str(DIALOGUE_DIR / f"{sid}.json"),
            *map(str, args),
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return json.loads(out)


def _py(sid, topic, pick, reflect, early_after):
    script, st, n = SCRIPTS[sid], d.new_state(SCRIPTS[sid], topic), 0
    while st["phase"] != "done":
        if early_after >= 0 and n == early_after:
            d.finish_early(script, st)
            n += 1000
            continue
        opts = d.options(script, st)
        d.choose(script, st, opts[reflect if st["phase"] == "reflection" else pick % len(opts)][0])
        n += 1
    return st


@needs_node
@pytest.mark.parametrize("sid", list(SCRIPTS))
@pytest.mark.parametrize("topic_idx", range(5))
@pytest.mark.parametrize(
    ("pick", "reflect", "early"), [(0, 0, -1), (1, 1, -1), (5, 2, -1), (0, 0, 0), (2, 0, 5)]
)
def test_js_and_python_dialogue_engines_are_identical(sid, topic_idx, pick, reflect, early):
    topic = SCRIPTS[sid].order[topic_idx]
    assert _js(sid, topic, pick, reflect, early) == _py(sid, topic, pick, reflect, early)


CASES = [
    ("evet", "stance", "evet"),
    ("Hayır, bence değil", "stance", "hayir"),
    ("Bilmiyorum", "stance", "kararsizim"),
    ("emin değilim", "stance", "kararsizim"),
    ("Kararsızım", "stance", "kararsizim"),
    ("kendi gözlemlerime dayanıyor", "reason", "experience"),
    ("somut bir örnek var", "reason", "example"),
    ("böyle duydum", "reason", "heard"),
    ("bir akıl yürütmeye dayanıyor", "reason", "reasoning"),
    ("inandığım bir ilkeye dayanıyor", "reason", "principle"),
    ("emin değilim daha çok düşünmeliyim", "reason", "unsure"),
    ("düşüncem değişti", "reflection", "changed"),
    ("düşüncem değişmedi", "reflection", "same"),
    ("henüz karar veremedim", "reflection", "undecided"),
    ("yapay zekâ olsun", "topic", "yapay-zeka"),
    ("adalet", "topic", "adalet"),
    ("rastgele bir şey", "stance", None),
]


@needs_node
def test_turkish_voice_matching_and_commands():
    s = SCRIPTS["sokrates"]

    def options(phase):
        if phase == "topic":
            return [{"id": t, "label": s.topics[t]["menu"]} for t in s.order]
        return [
            {"id": i, "label": label}
            for i, label in d.options(s, {"phase": phase, "topic": "bilgi"})
        ]

    payload = [{"transcript": t, "options": options(ph)} for t, ph, _ in CASES]
    payload += [
        {"transcript": "konuyu değiştirmek istiyorum", "command": True},
        {"transcript": "tekrar söyler misin", "command": True},
        {"transcript": "sus", "command": True},
    ]
    out = json.loads(
        subprocess.run(
            [NODE, str(ROOT / "tests/js/speech_runner.cjs")],
            input=json.dumps(payload),
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )
    assert out == [c[2] for c in CASES] + ["early", "repeat", "stop"]


def test_build_is_self_contained(tmp_path, monkeypatch):
    monkeypatch.setattr(build_vr, "OUT", tmp_path / "x.html")
    html = build_vr.build().read_text(encoding="utf-8")
    assert "/*__" not in html and "Mutluluk (Saadet)" in html and "Lykeion" in html
    assert not re.search(r'(?:src|href)="https?://', html)
    assert len(html) < 2_500_000


def test_committed_build_is_up_to_date(tmp_path, monkeypatch):
    committed = build_vr.OUT.read_text(encoding="utf-8")
    monkeypatch.setattr(build_vr, "OUT", tmp_path / "x.html")
    assert build_vr.build().read_text(encoding="utf-8") == committed, (
        "python scripts/build_vr.py çalıştırın"
    )


def test_browser_smoke_all_three_scenes():
    sync_api = pytest.importorskip("playwright.sync_api")
    with sync_api.sync_playwright() as p:
        try:
            b = p.chromium.launch(
                args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
            )
        except Exception as exc:
            pytest.skip(f"tarayıcı başlatılamadı: {type(exc).__name__}")
        page, errors = b.new_page(), []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(build_vr.OUT.resolve().as_uri())
        page.wait_for_selector("#options button")
        for sid in SCRIPTS:
            page.evaluate(f"AGORA.load('{sid}')")
            page.click("#options button >> nth=0")
            for _ in range(80):
                if page.evaluate("AGORA.state().phase") == "done":
                    break
                page.evaluate("()=>AGORA.choose(AGORA.view().options[0].id)")
            assert page.evaluate("AGORA.state().answers.length") == 6, sid
        assert not errors
        b.close()
