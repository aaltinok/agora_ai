"""Oturum dışa aktarma: Markdown ve (yazdır → PDF) için güvenli HTML."""

from __future__ import annotations

import datetime as dt
import html
from collections.abc import Sequence
from pathlib import Path

FONT_DIR = Path(__file__).resolve().parent.parent / "data" / "fonts"

JOURNAL = (
    "Tarih ve konu:\nKullanılan persona:\nBaşlangıç iddiam:\nEn güçlü gerekçe:\nEn güçlü itiraz:\n"
    "Değişen veya netleşen düşüncem:\nDoğrulanması gereken olgular:\nBir sonraki soru:"
)


def _now() -> str:
    return f"{dt.datetime.now():%d.%m.%Y %H:%M}"


def to_markdown(name: str, history: Sequence[dict], note: str = "", summary: str = "") -> str:
    lines = [f"# Oturum — {name}", f"Tarih: {_now()}", ""]
    lines += [f"**{'Ben' if m['role'] == 'user' else name}:** {m['content']}\n" for m in history]
    if note:
        lines += ["## Notlarım", note, ""]
    if summary:
        lines += ["## Özet", summary]
    return "\n".join(lines)


def to_html(name: str, history: Sequence[dict], note: str = "", summary: str = "") -> str:
    esc = html.escape
    rows = "".join(
        f"<p><b>{'Ben' if m['role'] == 'user' else esc(name)}:</b> {esc(m['content'])}</p>"
        for m in history
    )
    extra = (f"<h2>Notlarım</h2><p>{esc(note)}</p>" if note else "") + (
        f"<h2>Özet</h2><p>{esc(summary)}</p>" if summary else ""
    )
    return (
        '<!doctype html><html lang="tr"><meta charset="utf-8">'
        f"<title>Oturum — {esc(name)}</title>"
        "<style>body{font:16px/1.6 Georgia,serif;max-width:42rem;margin:2rem auto;padding:0 1rem}"
        "@media print{body{margin:0}}</style>"
        f"<h1>Oturum — {esc(name)}</h1><small>{_now()}</small>{rows}{extra}</html>"
    )


def to_pdf(
    name: str, history: Sequence[dict], note: str = "", summary: str = "", title: str = ""
) -> bytes:
    """PDF (Türkçe karakter destekli, DejaVu Sans). fpdf2 gerekir."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_font("DejaVu", "", str(FONT_DIR / "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", str(FONT_DIR / "DejaVuSans-Bold.ttf"))
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()

    def para(text: str, bold: bool = False, size: int = 11) -> None:
        pdf.set_font("DejaVu", "B" if bold else "", size)
        pdf.multi_cell(0, 6, text.replace("**", ""), new_x="LMARGIN", new_y="NEXT")

    para(title or f"Oturum: {name}", bold=True, size=16)
    para(f"Tarih: {_now()}")
    pdf.ln(3)
    for m in history:
        who = "Ben" if m["role"] == "user" else name
        para(f"{who}:", bold=True)
        para(m["content"])
        pdf.ln(1)
    if note:
        pdf.ln(2)
        para("Notlarım", bold=True)
        para(note)
    if summary:
        pdf.ln(2)
        para("Özet", bold=True)
        para(summary)
    return bytes(pdf.output())
