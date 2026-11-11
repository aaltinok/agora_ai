import pytest

from config.paths import QA_BANK_PATH, QA_VR_PATH
from philosophers.registry import get_registry
from services.qa_bank import QABank


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    for key in list(__import__("os").environ):
        if key.startswith("AGORA_"):
            monkeypatch.delenv(key)


@pytest.fixture(scope="session")
def registry():
    return get_registry()


@pytest.fixture(scope="session")
def bank(registry):
    return QABank.from_files([QA_BANK_PATH, QA_VR_PATH], known=set(registry.names))
