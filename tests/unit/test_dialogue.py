import copy
import json

import pytest

from config.paths import DIALOGUE_DIR
from services import dialogue as d

SCRIPTS = d.load_scripts(DIALOGUE_DIR)
IDS = list(SCRIPTS)


def _run(script, topic, pick=0, *, reflect=0):
    st = d.new_state(script, topic)
    while st["phase"] != "done":
        opts = d.options(script, st)
        d.choose(script, st, opts[reflect if st["phase"] == "reflection" else pick % len(opts)][0])
    return st


def test_three_scenarios_in_order():
    assert IDS == ["sokrates", "aristoteles", "farabi"]
    assert [s.scene for s in SCRIPTS.values()] == ["agora", "lykeion", "majlis"]
    assert all(s.setting and s.disclaimer for s in SCRIPTS.values())


@pytest.mark.parametrize("sid", IDS)
def test_six_questions_per_topic_and_six_reasons(sid):
    s = SCRIPTS[sid]
    assert len(s.order) == 5 and len(s.reasons) == 6
    for t in s.topics.values():
        assert len(t["questions"]) == 6, (sid, t["id"])
        assert all(len(q["branches"]) == 3 for q in t["questions"])


@pytest.mark.parametrize("sid", IDS)
def test_all_text_is_well_formed(sid):
    s = SCRIPTS[sid]
    seen = set()
    for t in s.topics.values():
        for q in t["questions"]:
            assert q["text"].endswith("?") and q["text"] not in seen
            seen.add(q["text"])
            assert all(b.endswith("?") for b in q["branches"].values()), q["id"]
    assert all(r["reply"].endswith("?") or r["reply"].endswith(".") for r in s.reasons)


@pytest.mark.parametrize("sid", IDS)
def test_period_rules_no_modern_words_no_verdicts(sid):
    blob = json.dumps(
        json.loads((DIALOGUE_DIR / f"{sid}.json").read_text(encoding="utf-8")), ensure_ascii=False
    ).lower()
    for verdict in ("doğru söyledin", "yanlış söyledin", "haklısın", "yanlışsın", "tebrikler"):
        assert verdict not in blob
    if (
        sid != "sokrates"
    ):  # Sokrates senaryosundaki Yapay Zekâ konusu belgede varsayımsal olarak işaretlidir
        for word in ("internet", "telefon", "bilgisayar", "yapay zek"):
            assert word not in blob, (sid, word)


@pytest.mark.parametrize("sid", IDS)
@pytest.mark.parametrize("pick", [0, 1, 2, 5])
def test_full_run_every_topic_and_branch(sid, pick):
    s = SCRIPTS[sid]
    for topic in s.order:
        st = _run(s, topic, pick)
        assert len(st["answers"]) == 6 and all(a["reason"] for a in st["answers"])
        assert st["reflection"] and st["log"][-1]["text"] == s.reflection["final"]
        assert all(t["who"] in ("philosopher", "student") for t in st["log"])


def test_philosopher_never_repeats_a_line_within_a_topic():
    for s in SCRIPTS.values():
        for topic in s.order:
            lines = [t["text"] for t in _run(s, topic)["log"] if t["who"] == "philosopher"]
            fixed = {r["reply"] for r in s.reasons} | {s.reason_prompt}
            uniq = [x for x in lines if x not in fixed]
            assert len(uniq) == len(set(uniq))


def test_counter_question_follows_the_chosen_stance():
    s = SCRIPTS["farabi"]
    st = d.new_state(s, "akil")
    d.choose(s, st, "evet")
    assert st["log"][-2]["text"] == s.topics["akil"]["questions"][0]["branches"]["evet"]
    assert st["phase"] == "reason" and st["log"][-1]["text"] == s.reason_prompt


def test_invalid_choice_unknown_topic_and_early_finish():
    s = SCRIPTS["sokrates"]
    st = d.new_state(s, "bilgi")
    with pytest.raises(d.DialogueError):
        d.choose(s, st, "yanlis")
    with pytest.raises(d.DialogueError):
        d.new_state(s, "yok")
    st = d.new_state(s, "adalet")
    d.finish_early(s, st)
    assert st["phase"] == "done"
    st = d.new_state(s, "adalet")
    d.choose(s, st, "hayir")
    d.finish_early(s, st)
    assert st["phase"] == "reflection" and st["answers"][0]["reason"] == "(gerekçe verilmedi)"


def test_summary_markdown_uses_script_title():
    md = d.summary_markdown(SCRIPTS["aristoteles"], _run(SCRIPTS["aristoteles"], "erdem"))
    assert "# Aristoteles ile Yüz Yüze — Erdem ve Altın Orta" in md


def test_validation_rejects_broken_scripts():
    data = json.loads((DIALOGUE_DIR / "farabi.json").read_text(encoding="utf-8"))
    bad = copy.deepcopy(data)
    del bad["topics"][0]["questions"][0]["branches"]["hayir"]
    with pytest.raises(d.DialogueError):
        d.validate(bad)
    with pytest.raises(d.DialogueError):
        d.validate({})
    assert d.load_script("/yok/dosya.json") is None
