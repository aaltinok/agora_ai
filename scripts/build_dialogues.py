"""Senaryo JSON'larını üretir:  python scripts/build_dialogues.py
- Aristoteles ve Farabi: scripts/authored_dialogues.py kaynağından.
- Sokrates: Word taslağından üretilen JSON'a 6. soru ve 6 gerekçe seçeneği eklenir (idempotent).
"""

from __future__ import annotations

import json
from pathlib import Path

from scripts.authored_dialogues import (
    ARISTOTELES,
    FARABI,
    REASON_LABELS,
    REFLECTION_OPTIONS,
    SOKRATES_EXTRA_QUESTIONS,
    SOKRATES_REASON_REPLIES,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "dialogues"
SOKRATES_PATH = OUT_DIR / "sokrates.json"
BRANCH_KEYS = ("evet", "hayir", "kararsizim")


def _reasons(replies: dict[str, str]) -> list[dict]:
    return [{"id": i, "label": label, "reply": replies[i]} for i, label in REASON_LABELS]


def to_script(spec: dict) -> dict:
    topics = []
    for t in spec["topics"]:
        qs = [
            {
                "id": f"{t['id']}-{n}",
                "text": q[0],
                "branches": dict(zip(BRANCH_KEYS, q[1:], strict=True)),
            }
            for n, q in enumerate(t["questions"], 1)
        ]
        topics.append(
            {
                "id": t["id"],
                "menu": t["menu"],
                "title": t["title"],
                "opening": t["opening"],
                "questions": qs,
                "closing": t["closing"],
            }
        )
    return {
        "version": 2,
        "id": spec["id"],
        "philosopher": spec["philosopher"],
        "scene": spec["scene"],
        "title": spec["title"],
        "setting": spec["setting"],
        "disclaimer": spec["disclaimer"],
        "welcome": spec["welcome"],
        "topics": topics,
        "reason_prompt": spec["reason_prompt"],
        "reasons": _reasons(spec["reasons"]),
        "bridges": spec["bridges"],
        "reflection": {
            "question": spec["reflection_question"],
            "options": REFLECTION_OPTIONS,
            "final": spec["final"],
        },
        "authored_note": "Tüm içerik taslaktır; tarihsel ve felsefi doğruluk açısından uzman gözden geçirmesi gerekir.",
    }


def augment_sokrates(script: dict) -> dict:
    """Word taslağından gelen Sokrates senaryosunu 6 soru + 6 gerekçe olacak biçimde tamamlar."""
    script.update(
        version=2,
        id="sokrates",
        philosopher="Sokrates",
        scene="agora",
        title="Sokrates ile Yüz Yüze",
        setting="Atina Agorası, MÖ 5. yüzyıl",
        disclaimer="Mekân ve giysiler dönem bilgisine dayanan yaklaşık bir canlandırmadır; belgelenmiş bir görüntü değildir.",
    )
    for t in script["topics"]:
        if len(t["questions"]) < 6:
            q = SOKRATES_EXTRA_QUESTIONS[t["id"]]
            t["questions"].append(
                {
                    "id": f"{t['id']}-{len(t['questions']) + 1}",
                    "text": q[0],
                    "branches": dict(zip(BRANCH_KEYS, q[1:], strict=True)),
                }
            )
    for extra in (
        "Şimdi bir başka açıdan bakalım.",
        "Bu düşünceyi bir yana koyup yeni bir soruya geçelim.",
    ):
        if extra not in script["bridges"] and len(script["bridges"]) < 6:
            script["bridges"].append(extra)
    script["reasons"] = _reasons(SOKRATES_REASON_REPLIES)
    script["authored_note"] = (
        "Her konudaki 6. soru, 6 gerekçe seçeneği ve 4 köprü cümlesi belgede yoktur; "
        "taslak olarak eklenmiştir. Gözden geçirin."
    )
    return script


def write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    for spec in (ARISTOTELES, FARABI):
        write(OUT_DIR / f"{spec['id']}.json", to_script(spec))
    if SOKRATES_PATH.is_file():
        write(
            SOKRATES_PATH, augment_sokrates(json.loads(SOKRATES_PATH.read_text(encoding="utf-8")))
        )
    for p in sorted(OUT_DIR.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        print(
            p.name,
            len(d["topics"]),
            "konu",
            sum(len(t["questions"]) for t in d["topics"]),
            "soru",
            len(d["reasons"]),
            "gerekçe",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
