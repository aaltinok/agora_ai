"""Tema: ekran görüntüsündeki koyu lacivert arayüze en yakın görünüm (Streamlit üzerine CSS)."""

from __future__ import annotations

LOGO_SVG = (
    '<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg" fill="none" '
    'stroke="currentColor" stroke-width="3" stroke-linejoin="round">'
    '<path d="M6 22 32 8l26 14z"/><path d="M10 26h44M14 50V30M26 50V30M38 50V30M50 50V30M8 54h48M5 58h54"/></svg>'
)

DARK = {
    "bg": "#0b1730",
    "bg2": "#102248",
    "card": "#13264a",
    "card2": "#17305c",
    "line": "#2c4a8a",
    "text": "#e8eefc",
    "muted": "#9fb0d6",
    "accent": "#4f8cff",
    "side": "#0a1328",
    "bubble": "#1a3a74",
}
LIGHT = {
    "bg": "#f3f6ff",
    "bg2": "#e6edff",
    "card": "#ffffff",
    "card2": "#eef3ff",
    "line": "#c9d6f5",
    "text": "#0b1730",
    "muted": "#4b5d85",
    "accent": "#2f6fe0",
    "side": "#e9efff",
    "bubble": "#d7e4ff",
}


def css(theme: str) -> str:
    c = LIGHT if theme == "Açık" else DARK
    return f"""<style>
:root{{--bg:{c["bg"]};--bg2:{c["bg2"]};--card:{c["card"]};--card2:{c["card2"]};--line:{c["line"]};--text:{c["text"]};--muted:{c["muted"]};--accent:{c["accent"]};--side:{c["side"]};--bubble:{c["bubble"]}}}
.stApp{{background:linear-gradient(160deg,var(--bg) 0%,var(--bg2) 100%);color:var(--text)}}
.stApp,.stApp p,.stApp label,.stApp li,.stApp span,.stApp h1,.stApp h2,.stApp h3,.stApp h4{{color:var(--text)}}
header[data-testid="stHeader"]{{background:transparent}}
.block-container{{padding-top:1.6rem;max-width:1180px}}
section[data-testid="stSidebar"]{{background:var(--side);border-right:1px solid var(--line)}}
section[data-testid="stSidebar"] .stButton>button{{justify-content:flex-start;background:transparent;border:0;color:var(--muted);border-radius:10px;padding:.55rem .8rem}}
section[data-testid="stSidebar"] button,section[data-testid="stSidebar"] button div{{justify-content:flex-start!important;text-align:left!important}}
section[data-testid="stSidebar"] .stButton>button:hover{{background:var(--card);color:var(--text)}}
section[data-testid="stSidebar"] .stButton>button[kind="primary"]{{background:var(--card2);color:var(--text);border-left:3px solid var(--accent)}}
.brand{{display:flex;align-items:center;gap:.7rem;color:var(--text)}}
.brand b{{font-size:1.5rem;letter-spacing:.14em;font-weight:600}}
.brand small{{display:block;letter-spacing:.3em;font-size:.62rem;color:var(--muted)}}
.hero{{border-radius:16px;padding:3.2rem 2rem;border:1px solid var(--line);background-size:cover;background-position:center;margin-bottom:1rem}}
.hero h1{{font-size:2.1rem;margin:0 0 .4rem;color:#fff!important}}
.hero p{{color:#dbe6ff!important;margin:0}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem}}
.avatar{{width:84px;height:84px;border-radius:50%;object-fit:cover;border:2px solid var(--line);display:block;margin:0 auto .4rem}}
.pcard img{{width:100%;aspect-ratio:1;object-fit:cover;border-radius:12px;border:1px solid var(--line)}}
.pname{{font-weight:600;text-align:center;margin:.3rem 0 0}}
.ptag{{text-align:center;color:var(--muted);font-size:.85rem}}
.pdesc{{color:var(--muted);font-size:.85rem;margin:.3rem 0 .6rem}}
.quote{{font-style:italic;color:var(--muted);font-size:1.15rem;text-align:center;padding:1rem}}
.feat{{display:grid;grid-template-columns:repeat(5,1fr);gap:.8rem;margin-top:1rem}}
.feat div{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:.8rem;text-align:center;font-size:.85rem;color:var(--muted)}}
.ts{{display:block;text-align:right;font-size:.7rem;color:var(--muted);margin-top:.2rem}}
.stChatMessage{{background:var(--card);border:1px solid var(--line);border-radius:14px}}
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]){{flex-direction:row-reverse;background:var(--bubble);width:82%;margin-left:auto}}
div[data-testid="stChatInput"]{{border-radius:24px;border:1px solid var(--line)}}
.stButton>button[kind="primary"]{{background:var(--accent);border:0;color:#fff;border-radius:10px}}
.stButton>button{{border-radius:10px;border:1px solid var(--line)}}
.sumrow{{display:flex;gap:.6rem;color:var(--muted);margin:.2rem 0}} .sumrow b{{color:var(--text)}}
.listitem{{display:flex;justify-content:space-between;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:.8rem 1rem;margin-bottom:.5rem}}
.listitem small{{color:var(--muted);display:block}}
@media (max-width:800px){{.feat{{grid-template-columns:1fr 1fr}} .stChatMessage:has([data-testid="stChatMessageAvatarUser"]){{margin-left:0}} .hero{{padding:2rem 1rem}}}}
</style>"""
