from config.settings import Settings, load_settings


def test_defaults_are_offline_rule_engine():
    s = load_settings(env={})
    assert s.engine == "rule" and not s.uses_llm


def test_env_overrides():
    s = load_settings(env={"AGORA_ENGINE": "LLM", "AGORA_MAX_INPUT_CHARS": "300"})
    assert s.uses_llm and s.max_input_chars == 300


def test_repr_and_public_hide_key():
    s = Settings(llm_api_key="sk-supersecretvalue1234")
    assert "supersecret" not in repr(s)
    assert "supersecret" not in str(s.public())


def test_dotenv_is_read(tmp_path):
    f = tmp_path / ".env"
    f.write_text("AGORA_ENGINE=llm\n# yorum\nAGORA_LLM_MODEL='m1'\n", encoding="utf-8")
    s = load_settings(dotenv=f)
    assert s.engine == "llm" and s.llm_model == "m1"
