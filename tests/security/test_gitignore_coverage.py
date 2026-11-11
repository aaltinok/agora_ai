from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    ".env",
    ".streamlit/secrets.toml",
    "__pycache__/",
    ".venv/",
    "*.log",
    "exports/",
    "sessions/",
]


def test_gitignore_covers_sensitive_paths():
    lines = {ln.strip() for ln in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()}
    assert [r for r in REQUIRED if r not in lines] == []
    assert "!.env.example" in lines


def test_dockerignore_excludes_secrets():
    text = (ROOT / ".dockerignore").read_text(encoding="utf-8")
    assert ".env" in text and "secrets.toml" in text


def test_no_real_env_or_secrets_file_committed():
    assert not (ROOT / ".env").exists()
    assert not (ROOT / ".streamlit" / "secrets.toml").exists()
