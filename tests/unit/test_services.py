from services import argument, export, modes, retention, summary


def test_argument_analysis():
    a = argument.analyze("Herkes özgür olmalı, çünkü herkes kendi hayatından sorumludur.")
    assert a.claim.startswith("Herkes özgür") and len(a.premises) == 1
    assert any("Mutlak" in i for i in a.issues)
    b = argument.analyze("Adalet önemlidir")
    assert b.premises == [] and "Gerekçe belirtilmemiş" in b.issues[0]
    assert "**İddia:**" in argument.render(a)


def test_argument_premise_before_conclusion():
    a = argument.analyze("Kural haksız; bu yüzden uymamalıyız.")
    assert a.premises == ["Kural haksız"] and a.claim == "uymamalıyız"


def test_modes(registry):
    p = registry["Sokrates"]
    assert modes.apply("Normal diyalog", p, "x") is None
    for mode in (
        "Felsefi soru analizi",
        "Argüman değerlendirme",
        "Aporia modu",
        "Karşıt görüş denemesi",
    ):
        assert modes.apply(mode, p, "Başarı nedir?")


def test_summary_and_export():
    hist = [
        {"role": "user", "content": "Adalet nedir?"},
        {"role": "assistant", "content": "Peki, eşitlik nedir?"},
    ]
    s = summary.summarize(hist, "Sokrates")
    assert "adalet" in s and "eşitlik nedir?" in s
    assert summary.summarize([], "x").startswith("Henüz")
    html = export.to_html("Sokrates", [{"role": "user", "content": "<script>alert(1)</script>"}])
    assert "<script>" not in html and "&lt;script&gt;" in html
    assert "# Oturum — Sokrates" in export.to_markdown("Sokrates", hist)


def test_retention():
    state = {"chats": {"a": [1]}, "notes": {"a": "n"}, "summaries": {}, "last_activity": 0.0}
    assert not retention.purge_if_expired(state, 100, now=50)
    assert retention.purge_if_expired(state, 100, now=500)
    assert state["chats"] == {} and state["notes"] == {}


def test_llm_messages_exclude_safety_and_start_with_user():
    hist = [
        {"role": "assistant", "content": "selam"},
        {"role": "user", "content": "gizli", "kind": "safety"},
        {"role": "user", "content": "Adalet?"},
        {"role": "assistant", "content": "Peki?"},
    ]
    msgs = retention.llm_messages(hist, 10)
    assert msgs[0] == {"role": "user", "content": "Adalet?"} and len(msgs) == 2


def test_pdf_export_has_turkish_text():
    pdf = export.to_pdf(
        "Farabi",
        [
            {"role": "user", "content": "Çağdaş şehir ığ"},
            {"role": "assistant", "content": "Akıl nedir?"},
        ],
        "not",
        "özet",
    )
    assert pdf[:4] == b"%PDF" and len(pdf) > 3000


def test_library_and_workshop():
    from services import library

    assert set(library.PROFILES) == {"Sokrates", "Platon", "Aristoteles", "Epiktetos", "Farabi"}
    plan = library.workshop_plan("Adalet", 4, 50)
    assert "Felsefe Atölyesi: Adalet" in plan and plan.count("\n1.") == 1
    assert "Faal akıl" in library.GLOSSARY
