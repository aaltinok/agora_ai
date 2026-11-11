"""Sesli diyalog bileşeni: tarayıcı konuşma tanıma (tr-TR) ve konuşma okuma; yapılandırma gerektirmez."""

from __future__ import annotations

from pathlib import Path

import streamlit.components.v1 as components

_voice = components.declare_component(
    "agora_voice", path=str(Path(__file__).resolve().parent / "voice")
)


def voice_panel(speak: str = "", nonce: str = "", enabled: bool = True, key: str = "voice"):
    """Dönen değer: {"text": ..., "ts": ...} (yeni bir konuşma tanındığında) ya da None."""
    return _voice(speak=speak, nonce=nonce, enabled=enabled, key=key, default=None)
