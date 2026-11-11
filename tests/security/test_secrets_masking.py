import pytest

from utils.secrets import get_secret, mask, redact


def test_mask():
    assert mask("") == "" and mask(None) == ""
    assert mask("short") == "****"
    assert mask("sk-abcdefghijklmnop1234") == "***1234"


@pytest.mark.parametrize(
    "text",
    [
        "sk-abcdefghij1234",
        "gsk_abcdefghij1234",
        "hf_abcdefghij1234",
        "Authorization: Bearer abc.def-123456",
        "api_key=hunter2hunter2",
    ],
)
def test_redact_patterns(text):
    assert "[REDACTED]" in redact(text)


def test_redact_keeps_normal_text():
    assert redact("Adalet nedir?") == "Adalet nedir?"


def test_get_secret_prefers_env(monkeypatch):
    monkeypatch.setenv("X_TEST_SECRET", "değer")
    assert get_secret("X_TEST_SECRET") == "değer"
    assert get_secret("YOK_BOYLE_BIR_SIR", "varsayılan") == "varsayılan"
