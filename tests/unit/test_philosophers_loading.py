from pathlib import Path

import pytest

from config.loader import ConfigError, load_philosophers, validate
from philosophers.base import Philosopher
from philosophers.registry import Registry, get_registry

FIXTURE = Path(__file__).parent.parent / "fixtures" / "sample_philosophers.yaml"


def test_five_philosophers_with_specialised_classes(registry):
    assert registry.names == ["Sokrates", "Platon", "Aristoteles", "Epiktetos", "Farabi"]
    assert {type(p).__name__ for p in registry} == {
        "Socrates",
        "Plato",
        "Aristotle",
        "Epictetus",
        "Farabi",
    }


def test_unknown_key_uses_base_class():
    r = Registry(load_philosophers(FIXTURE))
    assert type(r["Test"]) is Philosopher
    assert get_registry(FIXTURE)["Test"].compose(["x"]) == "x nedir?"


@pytest.mark.parametrize("bad", [None, {}, {"a": 1}, {"a": {"name": "x"}}])
def test_invalid_config_rejected(bad):
    with pytest.raises(ConfigError):
        validate(bad)


def test_unknown_placeholder_rejected():
    cfg = load_philosophers(FIXTURE)
    cfg["test"]["opening"] = ["{__class__}"]
    with pytest.raises(ConfigError):
        validate(cfg)


@pytest.mark.parametrize("turn", [0, 1, 2, 3])
def test_every_template_respects_character_rules(registry, turn):
    for p in registry:
        claim = "adalet herkese eşit davranmaktır" if turn else None
        out = p.compose(["adalet"], claim, turn)
        assert p.check_character(out) == [], (p.name, turn, out)


def test_compose_is_not_a_format_string_injection(registry):
    out = registry["Platon"].compose(["x"], "{kw} {__class__} {0}", 1)
    assert "{__class__}" in out


def test_bank_answers_have_no_forbidden_content(registry, bank):
    for p in registry:
        for q, a in bank.entries(p.name):
            assert p.forbidden_content(a) == [], (p.name, q)


def test_character_checks_catch_violations(registry):
    assert registry["Sokrates"].check_character("Adalet budur.")
    assert registry["Farabi"].check_character("Merhaba nasılsın?")
    assert registry["Aristoteles"].forbidden_content("Platon der ki bu doğru")
