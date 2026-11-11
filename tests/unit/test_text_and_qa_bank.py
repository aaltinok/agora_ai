from services.qa_bank import QABank, parse
from utils.textnorm import fold, keywords, sentences, tr_lower, truncate_words


def test_turkish_casing():
    assert tr_lower("ISPARTA İZMİR") == "ısparta izmir"
    assert fold("ÇOCUK Şiir") == "cocuk siir"


def test_keywords_and_helpers():
    assert keywords("Adalet nedir?") == ["adalet"]
    assert len(sentences("Bir. İki? Üç!")) == 3
    assert truncate_words("a " * 100, 10).endswith("…")


def test_parse_format():
    b = parse('1. "Adalet nedir?"\nSokrates: "Peki?"\n2. "x"\nYabancı: "y"\n', known={"Sokrates"})
    assert b == {"Sokrates": [("Adalet nedir?", "Peki?")]}


def test_matching(bank):
    assert bank.best_match("Sokrates", "ADALET NEDİR?").question == "Adalet nedir?"
    assert bank.best_match("Sokrates", "adalet ne demek").question == "Adalet nedir?"
    assert bank.best_match("Platon", "kuantum bilgisayarlar") is None


def test_shots_closest_first(bank):
    assert bank.shots("Aristoteles", "cesaret", k=1)[0][0] == "Cesaret nedir?"


def test_empty_and_duplicates():
    assert len(QABank.from_file("/yok/dosya.md")) == 0
    dup = QABank({"A": [("Soru?", "x"), ("soru?", "y")]})
    assert dup.duplicates() == [("A", "soru?")]
