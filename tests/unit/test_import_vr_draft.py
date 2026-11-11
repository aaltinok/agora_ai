import pytest

pytest.importorskip("docx")
from scripts import import_vr_draft as imp

PARAS = [
    "E. Sokrates Günümüzde Yaşasaydı",
    "24. Yapay zekâ hakkında ne düşünüyorsun?",
    'Sokrates: "Bu teknoloji benim çağımda yoktu."',
    "ADALET DİYALOĞU",
    "Sokrates'in açılışı:",
    '"Gel, adaleti araştıralım."',
    "1. Soru: Herkes eşit midir?",
    'Evet: "Neden?"',
    'Hayır: "Öyleyse?"',
    'Kararsızım: "Bir örnek?"',
    "Kapanış – Sokrates:",
    '"Hoşça kal."',
    "VR UYGULAMASINDA SORULAR NASIL İLERLEYECEK?",
]


def test_clean_and_unquote():
    assert imp.clean("a\u2019b \t c") == "a'b c"
    assert imp.unquote(' "Merhaba" ') == "Merhaba"


def test_parse_qa_marks_hypothetical_section():
    qa = imp.parse_qa(PARAS, 3)
    assert qa == [
        {
            "question": "Yapay zekâ hakkında ne düşünüyorsun?",
            "answer": "Bu teknoloji benim çağımda yoktu.",
            "section": "Sokrates Günümüzde Yaşasaydı",
            "hypothetical": True,
        }
    ]


def test_parse_topics():
    (t,) = imp.parse_topics(PARAS, 3, len(PARAS) - 1)
    assert t["id"] == "adalet" and t["opening"] == "Gel, adaleti araştıralım."
    assert t["questions"][0]["branches"] == {
        "evet": "Neden?",
        "hayir": "Öyleyse?",
        "kararsizim": "Bir örnek?",
    }
    assert t["closing"] == "Hoşça kal."
