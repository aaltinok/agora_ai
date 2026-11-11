"""philosophers.yaml yükleyici ve şema doğrulayıcı."""

from __future__ import annotations

import string
from pathlib import Path
from typing import Any

import yaml

from config.paths import PHILOSOPHERS_YAML

ALLOWED_PLACEHOLDERS = {"kw", "claim"}
_STR_FIELDS = ("name", "accent", "tag", "desc", "method", "style", "fallback")
_LIST_FIELDS = ("concepts", "opening", "followup")


class ConfigError(ValueError):
    """Bozuk veya eksik filozof yapılandırması."""


def _check_template(key: str, template: str) -> None:
    try:
        names = {f for _, f, _, _ in string.Formatter().parse(template) if f is not None}
    except ValueError as exc:
        raise ConfigError(f"{key}: şablon biçimi hatalı ({exc}).") from None
    if not names <= ALLOWED_PLACEHOLDERS:
        raise ConfigError(
            f"{key}: izin verilmeyen yer tutucu {sorted(names - ALLOWED_PLACEHOLDERS)}."
        )


def validate(data: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(data, dict) or not data:
        raise ConfigError("YAML kökü, filozof anahtarlarından oluşan bir sözlük olmalı.")
    for key, cfg in data.items():
        if not isinstance(cfg, dict):
            raise ConfigError(f"{key}: sözlük bekleniyordu.")
        for f in _STR_FIELDS:
            if not isinstance(cfg.get(f), str) or not cfg[f].strip():
                raise ConfigError(f"{key}: '{f}' boş olmayan metin olmalı.")
        for f in _LIST_FIELDS:
            val = cfg.get(f)
            if not isinstance(val, list) or not val or not all(isinstance(v, str) for v in val):
                raise ConfigError(f"{key}: '{f}' boş olmayan metin listesi olmalı.")
        for f in ("uncertain",):
            val = cfg.get(f, [])
            if not isinstance(val, list) or not all(isinstance(v, str) for v in val):
                raise ConfigError(f"{key}: '{f}' metin listesi olmalı.")
        if not isinstance(cfg.get("farewell", ""), str):
            raise ConfigError(f"{key}: 'farewell' metin olmalı.")
        if not isinstance(cfg.get("max_sentences"), int) or cfg["max_sentences"] < 1:
            raise ConfigError(f"{key}: 'max_sentences' pozitif tam sayı olmalı.")
        for template in (*cfg["opening"], *cfg["followup"], *cfg.get("uncertain", [])):
            _check_template(key, template)
    return data


def load_philosophers(path: Path | str = PHILOSOPHERS_YAML) -> dict[str, dict[str, Any]]:
    p = Path(path)
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigError(f"{p.name} okunamadı: {type(exc).__name__}") from None
    return validate(data)
