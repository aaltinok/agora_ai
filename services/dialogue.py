"""Sokrates'le Yüz Yüze: dallanan diyalog senaryosu ve durum makinesi.

Saf mantık (Streamlit/LLM yok): aynı JSON, VR motorunda (Unity/WebXR) da yüklenebilir.
Akış: Sokrates sorusu → öğrenci seçimi → karşı soru + "Neden?" → gerekçe seçimi →
köprü + yeni soru … → kapanış → düşünce değişti mi? → son söz.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

STANCES = (("evet", "Evet"), ("hayir", "Hayır"), ("kararsizim", "Kararsızım"))
PHASES = ("stance", "reason", "reflection", "done")


class DialogueError(ValueError):
    """Bozuk senaryo ya da geçersiz seçim."""


ORDER = ("sokrates", "aristoteles", "farabi")


@dataclass(frozen=True)
class Script:
    id: str
    philosopher: str
    scene: str
    title: str
    setting: str
    disclaimer: str
    welcome: str
    topics: dict[str, dict[str, Any]]
    order: tuple[str, ...]
    reason_prompt: str
    reasons: tuple[dict[str, str], ...]
    bridges: tuple[str, ...]
    reflection: dict[str, Any]


def validate(data: Any) -> Script:
    try:
        topics = {t["id"]: t for t in data["topics"]}
        for t in topics.values():
            if not t["questions"] or not t["opening"] or not t["closing"]:
                raise DialogueError(f"{t['id']}: eksik alan.")
            for q in t["questions"]:
                if set(q["branches"]) != {k for k, _ in STANCES} or not all(q["branches"].values()):
                    raise DialogueError(
                        f"{q['id']}: Evet/Hayır/Kararsızım dallarının üçü de dolu olmalı."
                    )
        script = Script(
            id=data["id"],
            philosopher=data["philosopher"],
            scene=data["scene"],
            title=data["title"],
            setting=data["setting"],
            disclaimer=data["disclaimer"],
            welcome=data["welcome"],
            topics=topics,
            order=tuple(t["id"] for t in data["topics"]),
            reason_prompt=data["reason_prompt"],
            reasons=tuple(data["reasons"]),
            bridges=tuple(data["bridges"]),
            reflection=data["reflection"],
        )
        if not script.reasons or not script.bridges or len(script.reflection["options"]) != 3:
            raise DialogueError("gerekçe, köprü ve 3 düşünce seçeneği gerekli.")
        return script
    except (KeyError, TypeError) as exc:
        raise DialogueError(f"Senaryo şeması geçersiz: {exc!r}") from None


def load_script(path: Path | str) -> Script | None:
    p = Path(path)
    if not p.is_file():
        return None
    try:
        return validate(json.loads(p.read_text(encoding="utf-8")))
    except json.JSONDecodeError:
        raise DialogueError(f"{p.name} geçerli JSON değil.") from None


def load_scripts(directory: Path | str) -> dict[str, Script]:
    """Klasördeki bütün senaryoları {id: Script} olarak yükler (ORDER sırasıyla)."""
    d = Path(directory)
    found = {}
    for p in sorted(d.glob("*.json")):
        script = load_script(p)
        if script is not None:
            found[script.id] = script
    return {k: found[k] for k in ORDER if k in found} | {
        k: v for k, v in found.items() if k not in ORDER
    }


# ---------------------------------------------------------------- durum makinesi
def _say(state: dict, who: str, text: str) -> None:
    state["log"].append({"who": who, "text": text})


def new_state(script: Script, topic_id: str) -> dict:
    if topic_id not in script.topics:
        raise DialogueError("Bilinmeyen konu.")
    topic = script.topics[topic_id]
    state = {
        "topic": topic_id,
        "q": 0,
        "phase": "stance",
        "log": [],
        "answers": [],
        "bridge": 0,
        "reflection": "",
    }
    _say(state, "philosopher", topic["opening"])
    _say(state, "philosopher", topic["questions"][0]["text"])
    return state


def options(script: Script, state: dict) -> list[tuple[str, str]]:
    phase = state["phase"]
    if phase == "stance":
        return list(STANCES)
    if phase == "reason":
        return [(r["id"], r["label"]) for r in script.reasons]
    if phase == "reflection":
        return [(o["id"], o["label"]) for o in script.reflection["options"]]
    return []


def _label(script: Script, state: dict, option_id: str) -> str:
    for oid, label in options(script, state):
        if oid == option_id:
            return label
    raise DialogueError("Bu adımda geçersiz seçim.")


def choose(script: Script, state: dict, option_id: str) -> dict:
    label = _label(script, state, option_id)
    topic = script.topics[state["topic"]]
    question = topic["questions"][state["q"]]
    _say(state, "student", label)
    if state["phase"] == "stance":
        state["answers"].append({"question": question["text"], "stance": label, "reason": ""})
        _say(state, "philosopher", question["branches"][option_id])
        _say(state, "philosopher", script.reason_prompt)
        state["phase"] = "reason"
    elif state["phase"] == "reason":
        state["answers"][-1]["reason"] = label
        _say(state, "philosopher", next(r["reply"] for r in script.reasons if r["id"] == option_id))
        if state["q"] + 1 < len(topic["questions"]):
            _say(state, "philosopher", script.bridges[state["bridge"] % len(script.bridges)])
            state["bridge"] += 1
            state["q"] += 1
            _say(state, "philosopher", topic["questions"][state["q"]]["text"])
            state["phase"] = "stance"
        else:
            _close(script, state)
    else:  # reflection
        state["reflection"] = label
        _say(state, "philosopher", script.reflection["final"])
        state["phase"] = "done"
    return state


def _close(script: Script, state: dict) -> None:
    _say(state, "philosopher", script.topics[state["topic"]]["closing"])
    _say(state, "philosopher", script.reflection["question"])
    state["phase"] = "reflection"


def finish_early(script: Script, state: dict) -> dict:
    """Öğrenci konuyu değiştirmek ister: tartışma uzatılmaz, kapanışa geçilir."""
    if state["phase"] in ("stance", "reason"):
        _say(state, "student", "Konuyu değiştirmek istiyorum.")
        if state["phase"] == "reason" and state["answers"] and not state["answers"][-1]["reason"]:
            state["answers"][-1]["reason"] = "(gerekçe verilmedi)"
        if state["answers"]:
            _close(script, state)
        else:
            _say(state, "philosopher", script.reflection["final"])
            state["phase"] = "done"
    return state


def summary_markdown(script: Script, state: dict) -> str:
    topic = script.topics[state["topic"]]
    lines = [f"# {script.title} — {topic['title']}", ""]
    for n, a in enumerate(state["answers"], 1):
        lines += [
            f"**{n}. {a['question']}**",
            f"- Seçim: {a['stance']}",
            f"- Gerekçe: {a['reason'] or '—'}",
            "",
        ]
    lines.append(f"**Düşünce değişimi:** {state['reflection'] or '—'}")
    return "\n".join(lines)
