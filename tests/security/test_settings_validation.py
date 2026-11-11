import pytest

from config.settings import SettingsError, load_settings


@pytest.mark.parametrize(
    "env",
    [
        {"AGORA_ENGINE": "gpt"},
        {"AGORA_LLM_BASE_URL": "ftp://localhost"},
        {"AGORA_LLM_BASE_URL": "http://example.com/v1"},  # uzak + http
        {"AGORA_LLM_BASE_URL": "https://user:pw@example.com/v1"},  # URL'de kimlik bilgisi
        {"AGORA_LLM_BASE_URL": "not a url"},
        {"AGORA_MAX_INPUT_CHARS": "5"},
        {"AGORA_MAX_INPUT_CHARS": "abc"},
        {"AGORA_RATE_LIMIT_PER_MIN": "0"},
        {"AGORA_LOG_LEVEL": "TRACE"},
    ],
)
def test_invalid_settings_rejected(env):
    with pytest.raises(SettingsError):
        load_settings(env=env)


@pytest.mark.parametrize(
    "url", ["http://localhost:11434/v1", "http://127.0.0.1:1234/v1", "https://api.example.com/v1"]
)
def test_valid_urls_accepted(url):
    assert load_settings(env={"AGORA_LLM_BASE_URL": url}).llm_base_url == url
