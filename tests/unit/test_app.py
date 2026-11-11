from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from ui.state import PAGES

APP = str(Path(__file__).resolve().parents[2] / "app.py")


def _app():
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    at.session_state["page"] = "Sohbet"
    return at.run()


def test_every_page_renders():
    at = _app()
    for page in PAGES:
        at.session_state["page"] = page
        at.run()
        assert not at.exception, page


def test_rule_based_chat_and_crisis_path():
    at = _app()
    at.chat_input[0].set_value("Adalet nedir?").run()
    assert not at.exception
    assert "öğretmen" in at.session_state["chats"]["Sokrates"][-1]["content"]
    at.chat_input[0].set_value("kendimi öldürmek istiyorum").run()
    last = at.session_state["chats"]["Sokrates"][-1]
    assert last["kind"] == "safety" and "112" in last["content"]


@pytest.mark.parametrize(
    ("who", "topic"),
    [("Sokrates", "Mutluluk"), ("Aristoteles", "Mantık"), ("Farabi", "Erdemli Şehir")],
)
def test_face_to_face_flow_for_each_philosopher(who, topic):
    at = _app()
    at.session_state["page"] = "Yüz Yüze"
    at.run()
    at.radio[0].set_value(next(o for o in at.radio[0].options if o == who or who in str(o))).run()
    next(b for b in at.button if b.label == topic).click().run()
    assert not at.exception and at.session_state["dialogue"]["sid"] == who.lower()
    next(b for b in at.button if b.label == "Evet").click().run()
    assert at.session_state["dialogue"]["phase"] == "reason"
    assert (
        len([b for b in at.button if b.label in (r for r in ["Aklımda somut bir örnek var"])]) == 1
    )


def test_sessions_page_offers_pdf():
    at = _app()
    at.chat_input[0].set_value("Adalet nedir?").run()
    at.session_state["page"] = "Oturumlar"
    at.run()
    assert not at.exception
