"""VR taslağındaki "VR için konuşma kuralları"nın testleri."""

import json

from config.paths import DIALOGUE_DIR
from llm.rule_based import RuleBasedProvider
from services import followups


def _chat(rb, p, messages):
    hist, replies = [], []
    for m in messages:
        hist.append({"role": "user", "content": m})
        reply = rb.respond(p, hist)
        hist.append({"role": "assistant", "content": reply})
        replies.append(reply)
    return replies


def test_unknown_answer_does_not_end_the_conversation(registry, bank):
    rb = RuleBasedProvider(bank, delay=0)
    out = rb.respond(registry["Sokrates"], [{"role": "user", "content": "Bilmiyorum"}])
    assert "daha basit bir örnek" in out.lower() and out.endswith("?")
    assert followups.is_uncertain("Emin değilim") and not followups.is_uncertain(
        "Adalet herkese eşit davranmaktır diye düşünüyorum çünkü"
    )


def test_same_counter_question_is_never_repeated(registry, bank):
    rb = RuleBasedProvider(bank, delay=0)
    replies = _chat(rb, registry["Sokrates"], ["bence zenginlik önemli"] * 6)
    assert len(set(replies)) == len(replies)


def test_every_reply_ends_with_a_counter_question_and_does_not_judge(registry, bank):
    rb = RuleBasedProvider(bank, delay=0)
    s = registry["Sokrates"]
    for reply in _chat(
        rb,
        s,
        ["zenginlik mutluluk getirir", "evet", "çünkü para her şeyi alır", "bilmiyorum", "belki"],
    ):
        assert s.check_character(reply) == [], reply


def test_student_question_pool_gets_replies():
    last = "Bilgelik, her şeyi bildiğini düşünmek değildir. İnsan sınırlarını fark etmelidir. Üçüncü cümle."
    assert "Bilgelik, her şeyi" in followups.reply_for("Bunu biraz daha açıklar mısın?", last)
    for q in followups.STUDENT_QUESTIONS:
        assert followups.reply_for(q, last).endswith("?")
    assert followups.reply_for("alakasız bir mesaj") is None


def test_sokrates_farewell_matches_the_script_and_everyone_has_one(registry):
    final = json.loads((DIALOGUE_DIR / "sokrates.json").read_text(encoding="utf-8"))["reflection"][
        "final"
    ]
    assert registry["Sokrates"].farewell == final
    assert all(p.farewell for p in registry)
