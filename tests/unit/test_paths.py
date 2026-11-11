import pytest

from config.paths import DATA_DIR, QA_BANK_PATH, safe_join


def test_known_paths_exist():
    assert QA_BANK_PATH.is_file()


def test_safe_join_inside():
    assert safe_join(DATA_DIR, "texts", "qa_bank.md") == QA_BANK_PATH


@pytest.mark.parametrize("bad", ["../config", "texts/../../app.py", "/etc/passwd"])
def test_safe_join_blocks_traversal(bad):
    with pytest.raises(ValueError):
        safe_join(DATA_DIR, bad)
