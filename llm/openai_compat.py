"""OpenAI uyumlu sunucu sağlayıcısı (Ollama, LM Studio, llama.cpp, Groq vb.).

Ücretsiz yerel kullanım için önerilen: Ollama  →  `ollama pull qwen2.5:7b`
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterator, Sequence

import requests

from config.constants import MODES
from config.settings import Settings
from llm.base import Provider, ProviderError
from philosophers.base import Philosopher
from services import summary
from services.qa_bank import QABank

log = logging.getLogger("agora.llm")
_SUMMARY_SYSTEM = (
    "Diyaloğu Türkçe, 120 kelimeyi aşmadan özetle: ana iddia, gerekçeler, açık sorular."
)


class OpenAICompatProvider(Provider):
    is_llm = True

    def __init__(self, settings: Settings, bank: QABank) -> None:
        self._base = settings.llm_base_url.rstrip("/")
        self._model, self._key, self._timeout = (
            settings.llm_model,
            settings.llm_api_key,
            settings.llm_timeout_s,
        )
        self._bank = bank
        self.name = f"Yerel LLM ({settings.llm_model})"

    def _headers(self) -> dict[str, str]:
        h = {"Content-Type": "application/json"}
        if self._key:
            h["Authorization"] = f"Bearer {self._key}"
        return h

    def _post(self, payload: dict, stream: bool) -> requests.Response:
        try:
            resp = requests.post(
                f"{self._base}/chat/completions",
                json=payload,
                headers=self._headers(),
                stream=stream,
                timeout=(5, self._timeout),
            )
            resp.raise_for_status()
        except requests.RequestException as exc:  # URL/anahtar sızmasın diye yalnızca tür adı
            log.warning("llm_request_failed type=%s", type(exc).__name__)
            raise ProviderError(f"LLM isteği başarısız ({type(exc).__name__}).") from None
        resp.encoding = "utf-8"
        return resp

    def healthy(self) -> bool:
        try:
            return requests.get(f"{self._base}/models", headers=self._headers(), timeout=2).ok
        except requests.RequestException:
            return False

    def stream(self, philosopher: Philosopher, history: Sequence[dict], mode: str) -> Iterator[str]:
        shots = self._bank.shots(philosopher.name, history[-1]["content"])
        system = philosopher.system_prompt(MODES.get(mode, ""), shots)
        payload = {
            "model": self._model,
            "stream": True,
            "temperature": 0.7,
            "max_tokens": 600,
            "messages": [{"role": "system", "content": system}, *history],
        }
        with self._post(payload, stream=True) as resp:
            for line in resp.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    delta = json.loads(data)["choices"][0]["delta"].get("content")
                except (KeyError, IndexError, ValueError, AttributeError):
                    continue
                if delta:
                    yield delta

    def summarize(self, philosopher: Philosopher, history: Sequence[dict]) -> str:
        transcript = "\n".join(f"{m['role']}: {m['content']}" for m in history)
        payload = {
            "model": self._model,
            "stream": False,
            "max_tokens": 300,
            "messages": [
                {"role": "system", "content": _SUMMARY_SYSTEM},
                {"role": "user", "content": transcript},
            ],
        }
        try:
            with self._post(payload, stream=False) as resp:
                return resp.json()["choices"][0]["message"]["content"].strip()
        except (ProviderError, KeyError, IndexError, ValueError):
            return summary.summarize(history, philosopher.name)
