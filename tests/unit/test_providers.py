import json

import pytest
import requests

from config.settings import Settings
from llm import openai_compat
from llm.base import ProviderError
from llm.factory import FALLBACK_NOTICE, FallbackProvider, build_provider
from llm.openai_compat import OpenAICompatProvider
from llm.rule_based import RuleBasedProvider

HIST = [{"role": "user", "content": "Adalet nedir?"}]


class FakeResp:
    encoding = None

    def __init__(self, lines):
        self._lines = lines

    def raise_for_status(self):
        pass

    def iter_lines(self, decode_unicode=True):
        yield from self._lines

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def sse(*chunks):
    out = [f"data: {json.dumps({'choices': [{'delta': {'content': c}}]})}" for c in chunks]
    return [*out, "data: [DONE]"]


def test_rule_based_uses_bank_then_templates(registry, bank):
    rb = RuleBasedProvider(bank, delay=0)
    assert "öğretmen" in "".join(rb.stream(registry["Sokrates"], HIST, "Normal diyalog"))
    out = rb.respond(registry["Platon"], [{"role": "user", "content": "kuantum fiziği"}])
    assert "kuantum" in out
    hist = [
        *HIST,
        {"role": "assistant", "content": "x"},
        {"role": "user", "content": "bence eşitlik önemli"},
    ]
    out = rb.respond(registry["Sokrates"], hist)
    assert out.endswith("?") and out != "x"
    assert "eşitlik" in rb.respond(registry["Platon"], hist)
    assert (
        rb.respond(registry["Sokrates"], [{"role": "user", "content": "?!"}])
        == registry["Sokrates"].fallback
    )


def test_llm_stream_parses_sse(monkeypatch, registry, bank):
    seen = {}

    def fake_post(url, **kw):
        seen.update(url=url, **kw)
        return FakeResp(sse("Mer", "haba"))

    monkeypatch.setattr(openai_compat.requests, "post", fake_post)
    p = OpenAICompatProvider(Settings(engine="llm", llm_api_key="abc"), bank)
    assert "".join(p.stream(registry["Sokrates"], HIST, "Normal diyalog")) == "Merhaba"
    assert (
        seen["url"].endswith("/chat/completions")
        and seen["headers"]["Authorization"] == "Bearer abc"
    )
    assert seen["json"]["messages"][0]["role"] == "system"


def test_error_message_leaks_nothing(monkeypatch, registry, bank):
    def boom(url, **kw):
        raise requests.ConnectionError(f"failed {url} Bearer sk-secretsecret123")

    monkeypatch.setattr(openai_compat.requests, "post", boom)
    p = OpenAICompatProvider(Settings(engine="llm", llm_api_key="sk-secretsecret123"), bank)
    with pytest.raises(ProviderError) as e:
        list(p.stream(registry["Sokrates"], HIST, "Normal diyalog"))
    assert "secret" not in str(e.value) and "localhost" not in str(e.value)


def test_fallback_to_rule_engine(monkeypatch, registry, bank):
    monkeypatch.setattr(
        openai_compat.requests, "post", lambda *a, **k: (_ for _ in ()).throw(requests.Timeout())
    )
    prov = build_provider(Settings(engine="llm"), bank)
    assert isinstance(prov, FallbackProvider) and prov.is_llm
    text = "".join(prov.stream(registry["Sokrates"], HIST, "Normal diyalog"))
    assert text.startswith(FALLBACK_NOTICE) and "öğretmen" in text


def test_rule_engine_is_default(bank):
    assert isinstance(build_provider(Settings(), bank), RuleBasedProvider)


def test_llm_summary_falls_back(monkeypatch, registry, bank):
    monkeypatch.setattr(
        openai_compat.requests, "post", lambda *a, **k: (_ for _ in ()).throw(requests.Timeout())
    )
    p = OpenAICompatProvider(Settings(engine="llm"), bank)
    assert "Filozof" in p.summarize(registry["Sokrates"], HIST)
