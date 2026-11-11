import re
from pathlib import Path

from config.settings import load_settings
from utils.secrets import redact

ROOT = Path(__file__).resolve().parents[2]


def _pairs(name):
    for ln in (ROOT / name).read_text(encoding="utf-8").splitlines():
        if ln.strip() and not ln.startswith("#") and "=" in ln:
            k, _, v = ln.partition("=")
            yield k.strip(), v.strip().strip('"')


def test_env_example_has_no_secret_values():
    pairs = dict(_pairs(".env.example"))
    assert pairs["AGORA_LLM_API_KEY"] == ""
    for k, v in pairs.items():
        assert redact(f"{k}={v}") == f"{k}={v}", k


def test_env_example_is_a_valid_configuration():
    assert load_settings(env=dict(_pairs(".env.example"))).engine == "rule"


def test_secrets_example_is_empty():
    for _, v in _pairs(".streamlit/secrets.toml.example"):
        assert v == ""


def test_no_key_like_strings_in_source():
    pattern = re.compile(r"\b(?:sk|gsk|hf|ghp)[-_][A-Za-z0-9]{20,}")
    for f in ROOT.rglob("*.py"):
        if ".venv" in f.parts or "tests" in f.parts:
            continue
        assert not pattern.search(f.read_text(encoding="utf-8")), f
