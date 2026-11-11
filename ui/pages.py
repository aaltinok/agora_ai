"""Streamlit sayfaları (ekran görüntüsündeki tasarıma göre). Mantık services/llm katmanlarındadır."""

from __future__ import annotations

import datetime as dt
import html
from dataclasses import dataclass, field

import streamlit as st
import streamlit.components.v1 as components

from config.constants import MODES, PRINCIPLE, SIMULATION_NOTE
from config.paths import VR_DIST
from config.settings import Settings
from llm.base import Provider
from philosophers.registry import Registry
from services import argument, dialogue, export, followups, library, modes, pipeline, retention
from services.qa_bank import QABank
from ui import assets, theme
from ui.voice import voice_panel
from utils.textnorm import keywords, truncate_words


@dataclass(frozen=True)
class Ctx:
    settings: Settings
    registry: Registry
    bank: QABank
    provider: Provider
    rule_provider: Provider
    scripts: dict = field(default_factory=dict)


def H(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


def _now() -> str:
    return f"{dt.datetime.now():%H:%M}"


def _provider(ctx: Ctx) -> Provider:
    return ctx.rule_provider if st.session_state.force_rule else ctx.provider


def go(page: str, philosopher: str | None = None) -> None:
    st.session_state.page = page
    if philosopher:
        st.session_state.philosopher = philosopher


def submit(ctx: Ctx, name: str, raw: str) -> pipeline.Decision:
    """Girdiyi hattan geçirir; sohbet geçmişini günceller."""
    ss = st.session_state
    d = pipeline.pre_process(raw, max_chars=ctx.settings.max_input_chars, limiter=ss.limiter)
    hist = ss.chats.setdefault(name, [])
    if d.action == "proceed":
        hist.append({"role": "user", "content": d.clean, "ts": _now()})
        ss.pending = True
    elif d.reason != "empty":
        kind = "safety" if d.reason == "crisis" else "system"
        hist.append({"role": "user", "content": d.clean, "kind": kind, "ts": _now()})
        hist.append({"role": "assistant", "content": d.reply, "kind": kind, "ts": _now()})
    else:
        st.toast(d.reply)
    return d


def ask(ctx: Ctx, name: str, question: str) -> None:
    submit(ctx, name, question)
    go("Sohbet", name)


def reply_text(ctx: Ctx, name: str, msgs: list[dict], mode: str = "Normal diyalog") -> str:
    """Akışsız yanıt (karşılaştırma ve sesli diyalog için)."""
    p, prov = ctx.registry[name], _provider(ctx)
    respond = getattr(prov, "respond", None)
    return respond(p, msgs, mode) if respond else "".join(prov.stream(p, msgs, mode))


def _avatar(p, size: int = 84) -> str:
    return f'<img class="avatar" style="width:{size}px;height:{size}px;border-color:{p.accent}" src="{assets.portrait(p.key)}" alt="{html.escape(p.name)}">'


def _toast_reminder(ctx: Ctx, hist: list[dict]) -> None:
    n = sum(1 for m in hist if m["role"] == "user" and not m.get("kind"))
    if (
        st.session_state.reminders
        and n
        and n % 5 == 0
        and st.session_state.get("last_reminder") != n
    ):
        st.session_state.last_reminder = n
        st.toast("Bir ara verip şimdiye kadarki düşüncelerini özetlemek ister misin?")


# ------------------------------------------------------------------ Ana Sayfa
def home(ctx: Ctx) -> None:
    ss = st.session_state
    H(
        f'<div class="hero" style="background-image:linear-gradient(rgba(8,18,40,.55),rgba(8,18,40,.7)),url({assets.hero()})">'
        "<h1>Düşüncelerine yeni bir bakış açısı kazandır.</h1>"
        "<p>Beş büyük filozofla diyalog kur, sorularını derinleştir, düşünce gücünü geliştir.</p></div>"
    )
    c1, c2 = st.columns([9, 1])
    q = c1.text_input(
        "Felsefi bir konu seçin veya sorunuzu yazın...",
        label_visibility="collapsed",
        placeholder="Felsefi bir konu seçin veya sorunuzu yazın...",
        max_chars=ctx.settings.max_input_chars,
    )
    if (
        c2.button("", icon=":material/arrow_forward:", type="primary", width="stretch")
        and q.strip()
    ):
        ask(ctx, ss.philosopher, q)
        st.rerun()
    for col, p in zip(st.columns(len(ctx.registry)), ctx.registry, strict=False):
        with col:
            H(
                f'<div style="text-align:center">{_avatar(p)}<div class="pname">{html.escape(p.name)}</div><div class="ptag">{html.escape(p.tag)}</div></div>'
            )
            st.button(
                "Başla", key=f"home_{p.key}", on_click=go, args=("Sohbet", p.name), width="stretch"
            )
    H('<div class="quote">Gerçek bilgi, sorgulayan zihinde başlar.</div>')
    H(
        '<div class="feat"><div>Kişiselleştirilmiş öğrenme deneyimi</div><div>Zengin diyalog yapısı</div>'
        "<div>5 farklı filozof, 5 farklı bakış açısı</div><div>Güvenli ve seçimli veri kullanımı</div><div>Web ve mobil uyumlu</div></div>"
    )
    H('<div class="quote">Daha iyi sorular, daha derin düşünceler...</div>')
    st.caption(PRINCIPLE)


# ------------------------------------------------------------------ Filozoflar
def philosophers(ctx: Ctx) -> None:
    st.header("Filozofları Keşfet")
    items = list(ctx.registry)
    for row in (items[:3], items[3:]):
        for col, p in zip(st.columns(3), row, strict=False):
            with col:
                H(
                    f'<div class="card pcard"><img src="{assets.portrait(p.key)}" alt=""><div class="pname">{html.escape(p.name)}</div>'
                    f'<div class="ptag">{html.escape(p.tag)}</div><div class="pdesc">{html.escape(p.desc)}</div></div>'
                )
                with st.expander("Yöntem ve kaynaklar"):
                    prof = library.PROFILES.get(p.name, {})
                    st.markdown(
                        f"**Yöntem:** {p.method}\n\n**Kavramlar:** {', '.join(p.concepts)}\n\n"
                        f"**Dönem:** {prof.get('dönem', '-')}\n\n**Kaynaklar:** {prof.get('kaynak', '-')}"
                    )
                st.button(
                    "Diyalog başlat",
                    key=f"pick_{p.key}",
                    on_click=go,
                    args=("Sohbet", p.name),
                    type="primary",
                    width="stretch",
                )
    st.caption(SIMULATION_NOTE)


# ------------------------------------------------------------------ Sohbet
def chat(ctx: Ctx) -> None:
    ss = st.session_state
    names = ctx.registry.names
    a, b, c = st.columns([5, 2, 2])
    ss.philosopher = b.selectbox("Filozof", names, index=names.index(ss.philosopher))
    ss.mode = c.selectbox("Mod", list(MODES), index=list(MODES).index(ss.mode))
    p = ctx.registry[ss.philosopher]
    a.markdown(f"## {p.name} ile Dialog")
    hist = ss.chats.setdefault(p.name, [])
    avatar = str(assets.ASSETS / "portraits" / f"{p.key}.png")
    for m in hist:
        with st.chat_message(m["role"], avatar=None if m["role"] == "user" else avatar):
            st.markdown(m["content"])
            if m.get("ts"):
                H(f'<span class="ts">{m["ts"]}</span>')

    if prompt := st.chat_input("Sorunuzu yazın...", max_chars=ctx.settings.max_input_chars):
        d = submit(ctx, p.name, prompt)
        if d.action == "reply":
            st.rerun()
        with st.chat_message("user"):
            st.markdown(d.clean)
        if d.notice:
            st.caption(d.notice)
    if ss.pending and hist and hist[-1]["role"] == "user":
        ss.pending = False
        msgs = retention.llm_messages(hist, ctx.settings.max_history_messages)
        with st.chat_message("assistant", avatar=avatar):
            reply = st.write_stream(_provider(ctx).stream(p, msgs, ss.mode))
        hist.append({"role": "assistant", "content": reply, "ts": _now()})
        _toast_reminder(ctx, hist)
    if hist and hist[-1]["role"] == "assistant" and not ss.pending:
        if p.name == "Sokrates":
            st.caption("Sokrates'e sorabileceklerin:")
            for i, q in enumerate(followups.STUDENT_QUESTIONS):
                st.button(q, key=f"fq_{len(hist)}_{i}", on_click=ask, args=(ctx, p.name, q))
        if p.farewell and hist[-1]["content"] != p.farewell:
            st.button(
                "Konuşmayı bitir",
                key=f"bye_{len(hist)}",
                on_click=lambda: hist.append(
                    {"role": "assistant", "content": p.farewell, "ts": _now()}
                ),
            )
    st.caption(SIMULATION_NOTE)


# ------------------------------------------------------------------ Karşılaştırma
TOPICS = ["Adalet", "Mutluluk", "Erdem", "Bilgi", "Özgürlük", "Dostluk"]


def compare(ctx: Ctx) -> None:
    a, b = st.columns([3, 1])
    a.header("Filozofları Karşılaştır")
    topic = b.selectbox("Konu", TOPICS, label_visibility="collapsed")
    custom = st.text_input(
        "Ya da kendi sorun (isteğe bağlı)", max_chars=ctx.settings.max_input_chars
    )
    question = custom.strip() or f"{topic} nedir?"
    d = pipeline.pre_process(
        question, max_chars=ctx.settings.max_input_chars, limiter=st.session_state.limiter
    )
    if d.action == "reply":
        st.warning(d.reply)
        return
    for col, p in zip(st.columns(len(ctx.registry)), ctx.registry, strict=False):
        with col:
            text = truncate_words(
                reply_text(ctx, p.name, [{"role": "user", "content": d.clean}]), 230
            )
            H(
                f'<div class="card" style="min-height:260px">{_avatar(p, 64)}<div class="pname">{html.escape(p.name)}</div>'
                f'<div class="ptag">{html.escape(p.tag)}</div><div class="pdesc">{html.escape(text)}</div></div>'
            )
            st.button(
                "Detay",
                key=f"detail_{p.key}",
                on_click=ask,
                args=(ctx, p.name, d.clean),
                width="stretch",
            )


# ------------------------------------------------------------------ Oturumlar
def sessions(ctx: Ctx) -> None:
    ss = st.session_state
    st.header("Oturum Özeti")
    active = [n for n, h in ss.chats.items() if retention.conversation(h)]
    if not active:
        st.info("Henüz oturum yok.")
        return
    name = st.selectbox(
        "Oturum", active, index=active.index(ss.philosopher) if ss.philosopher in active else 0
    )
    p, conv = ctx.registry[name], retention.conversation(ss.chats[name])
    first = next((m["content"] for m in conv if m["role"] == "user"), "")
    topic = (keywords(first, 1) or ["-"])[0].capitalize()
    if st.button("Özet oluştur", type="primary"):
        ss.summaries[name] = _provider(ctx).summarize(p, conv)
    summary = ss.summaries.get(name, "")
    H(
        f'<div class="card"><div class="sumrow">Konu: <b>{html.escape(topic)}</b></div>'
        f'<div class="sumrow">Seçilen Filozof: <b>{html.escape(name)}</b></div>'
        f'<div class="sumrow">Tarih: <b>{dt.datetime.now():%d.%m.%Y %H:%M}</b></div></div>'
    )
    if summary:
        st.markdown(summary)
    ss.notes.setdefault(name, "")
    c1, c2, c3 = st.columns(3)
    with c1.popover("Not Ekle", width="stretch"):
        ss.notes[name] = st.text_area("Notlarım", ss.notes[name], key=f"note_{name}")
    pdf = export.to_pdf(name, conv, ss.notes[name], summary, f"Oturum: {name}")
    c2.download_button(
        "PDF Olarak İndir", pdf, f"agora_{p.key}.pdf", "application/pdf", width="stretch"
    )
    with c3.popover("Paylaş", width="stretch"):
        st.caption("Aşağıdaki metni kopyalayıp paylaşabilirsiniz.")
        st.code(export.to_markdown(name, conv, ss.notes[name], summary), language="markdown")
    with st.expander("Diğer biçimler"):
        st.download_button(
            "Markdown indir",
            export.to_markdown(name, conv, ss.notes[name], summary),
            f"agora_{p.key}.md",
        )
        st.download_button(
            "Yazdırılabilir HTML",
            export.to_html(name, conv, ss.notes[name], summary),
            f"agora_{p.key}.html",
        )


# ------------------------------------------------------------------ Sesli Diyalog
def voice_page(ctx: Ctx) -> None:
    ss = st.session_state
    st.header("Sesli Kullanım")
    st.caption("İstediğin zaman sesli olarak soru sorabilir ve yanıtları dinleyebilirsin.")
    names = ctx.registry.names
    ss.philosopher = st.selectbox("Filozof", names, index=names.index(ss.philosopher))
    name = ss.philosopher
    hist = ss.chats.setdefault(name, [])
    base = ss.voice_base.setdefault(name, len(hist))
    last = next(
        (m["content"] for m in reversed(hist) if m["role"] == "assistant" and not m.get("kind")), ""
    )
    speak = last if len(hist) > base and ss.voice_replies else ""
    res = voice_panel(
        speak=speak, nonce=str(len(hist)), enabled=bool(ss.voice_replies), key="voice_main"
    )
    if res and res.get("ts") != ss.voice_ts:
        ss.voice_ts = res["ts"]
        d = submit(ctx, name, res["text"])
        if d.action == "proceed":
            ss.pending = False
            msgs = retention.llm_messages(hist, ctx.settings.max_history_messages)
            hist.append(
                {"role": "assistant", "content": reply_text(ctx, name, msgs, ss.mode), "ts": _now()}
            )
        st.rerun()
    for m in hist[-4:]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    if not ss.voice_replies:
        st.caption(
            "Sesli yanıtlar Ayarlar sayfasından kapatılmış; yanıtlar yalnızca yazılı gösterilir."
        )


# ------------------------------------------------------------------ Yüz Yüze (senaryolu diyalog)
def _start(script_id: str, topic_id: str) -> None:
    script = st.session_state.scripts_ref[script_id]
    st.session_state.dialogue = {**dialogue.new_state(script, topic_id), "sid": script_id}


def _pick(option_id: str) -> None:
    ss = st.session_state
    dialogue.choose(ss.scripts_ref[ss.dialogue["sid"]], ss.dialogue, option_id)


def _early() -> None:
    ss = st.session_state
    dialogue.finish_early(ss.scripts_ref[ss.dialogue["sid"]], ss.dialogue)


def _reset() -> None:
    st.session_state.dialogue = {}


def face_to_face(ctx: Ctx) -> None:
    ss = st.session_state
    ss.scripts_ref = ctx.scripts
    st.header("Filozofla Yüz Yüze")
    if not ctx.scripts:
        st.warning(
            "data/dialogues klasöründe senaryo yok. python scripts/build_dialogues.py ile üretin."
        )
        return
    state = ss.dialogue
    ids = list(ctx.scripts)
    if not state:
        sid = st.radio(
            "Filozof", ids, format_func=lambda i: ctx.scripts[i].philosopher, horizontal=True
        )
        script = ctx.scripts[sid]
        st.markdown(f"*{script.setting}.* {script.welcome}")
        st.caption("Bir konu seç:")
        for col, tid in zip(st.columns(len(script.order)), script.order, strict=True):
            col.button(
                script.topics[tid]["menu"],
                key=f"topic_{sid}_{tid}",
                on_click=_start,
                args=(sid, tid),
                width="stretch",
            )
        st.caption(script.disclaimer)
        return
    script = ctx.scripts[state["sid"]]
    st.subheader(f"{script.philosopher}: {script.topics[state['topic']]['title']}")
    p = ctx.registry[script.philosopher]
    avatar = str(assets.ASSETS / "portraits" / f"{p.key}.png")
    for turn in state["log"]:
        is_bot = turn["who"] == "philosopher"
        with st.chat_message("assistant" if is_bot else "user", avatar=avatar if is_bot else None):
            st.markdown(turn["text"])
    opts = dialogue.options(script, state)
    if opts:
        st.caption("Cevabını seç:")
        for col, (oid, label) in zip(st.columns(min(len(opts), 3)), opts[:3], strict=False):
            col.button(
                label,
                key=f"opt_{len(state['log'])}_{oid}",
                on_click=_pick,
                args=(oid,),
                width="stretch",
            )
        for oid, label in opts[3:]:
            st.button(
                label,
                key=f"opt_{len(state['log'])}_{oid}",
                on_click=_pick,
                args=(oid,),
                width="stretch",
            )
        if state["phase"] in ("stance", "reason"):
            st.button(
                "Konuyu değiştirmek istiyorum", key=f"early_{len(state['log'])}", on_click=_early
            )
    else:
        md = dialogue.summary_markdown(script, state)
        with st.expander("Oturum özeti (öğretmen için)", expanded=True):
            st.markdown(md)
        st.download_button(
            "Özeti indir (Markdown)", md, f"yuz_yuze_{state['sid']}_{state['topic']}.md"
        )
        st.button("Yeni konu seç", on_click=_reset, type="primary")


# ------------------------------------------------------------------ 3B Agora
@st.cache_data
def _vr_html(mtime: float) -> str:
    return VR_DIST.read_text(encoding="utf-8")


def vr_agora(ctx: Ctx) -> None:
    st.header("3B Mekânlar: Atina Agorası, Lykeion, Abbasi İlim Meclisi")
    if not VR_DIST.is_file():
        st.warning("vr/dist/agora_vr.html yok. Üretmek için: python scripts/build_vr.py")
        return
    html_text = _vr_html(VR_DIST.stat().st_mtime)
    st.caption(
        "Sürükleyerek etrafına bak; üstten filozofu seç. Mikrofon için tarayıcı izin ister; VR için dosyayı ayrı sekmede ya da başlıkta açın."
    )
    if hasattr(st, "iframe"):  # Streamlit 1.5x+: yerel dosya gömme
        st.iframe(VR_DIST, height=740)
    else:
        components.html(html_text, height=740)
    st.download_button(
        "agora_vr.html indir (VR başlığında açmak için)", html_text, "agora_vr.html", "text/html"
    )
    with st.expander("VR başlığında ve okulda nasıl çalıştırılır?"):
        st.markdown(
            "1. Dosyayı **https** ya da `localhost` üzerinden sunun (WebXR ve mikrofon güvenli bağlam ister): "
            "`python -m http.server` ya da GitHub Pages.\n"
            "2. Quest Browser'da adresi açın, **VR'ye gir**. VR içinde seçim denetleyici ışınıyladır.\n"
            "3. Ses tanıma tarayıcıya bağlıdır (Chrome/Edge); Quest'te çalışmayabilir. Düğmeler her zaman çalışır.\n"
            "4. Ses tanıma sesi tarayıcı sağlayıcısına gönderebilir; öğrencilerle kullanmadan önce izin alın."
        )


# ------------------------------------------------------------------ Soru Bankası
def question_bank(ctx: Ctx) -> None:
    st.header("Soru-Cevap Bankası")
    if not len(ctx.bank):
        st.warning("data/texts/qa_bank.md bulunamadı veya boş.")
        return
    name = st.selectbox("Filozof", ctx.bank.philosophers)
    st.caption(f"{len(ctx.bank.entries(name))} soru")
    for i, (q, a) in enumerate(ctx.bank.entries(name)):
        with st.expander(q):
            st.markdown(f"**{name}:** {a}")
            st.button("Sohbette sor", key=f"bank_{name}_{i}", on_click=ask, args=(ctx, name, q))


# ------------------------------------------------------------------ İleri Düzey
ADV = [
    ("Felsefi Soru Analizörü", "Sorularını mantıksal yapılarına ayır."),
    ("Argüman Değerlendirme", "İddialarının güçlü ve zayıf yönlerini analiz et."),
    ("Aporia Modu", "Bilerek oluşturulan çıkmaz ile düşünceni derinleştir."),
    ("Felsefe Atölyesi", "Konulara özel çalışma planları oluştur."),
    ("Kütüphane", "Felsefe metinleri, kavramlar ve kaynaklara erişim sağla."),
]


def advanced(ctx: Ctx) -> None:
    ss = st.session_state
    st.header("İleri Düzey Özellikler")
    for title, desc in ADV:
        c1, c2 = st.columns([8, 1])
        c1.markdown(
            f'<div class="listitem"><div><b>{title}</b><small>{desc}</small></div></div>',
            unsafe_allow_html=True,
        )
        c2.button(
            "",
            key=f"adv_{title}",
            icon=":material/chevron_right:",
            on_click=lambda t=title: ss.update(adv=t),
        )
    st.divider()
    st.subheader(ss.adv)
    mx = ctx.settings.max_input_chars
    if ss.adv == "Felsefi Soru Analizörü":
        t = st.text_input("Sorunu yaz", "Başarı nedir?", max_chars=mx)
        if t.strip():
            st.markdown(modes.analyze_question(t))
    elif ss.adv == "Argüman Değerlendirme":
        t = st.text_area(
            "İddianı gerekçesiyle yaz",
            "Herkes özgür olmalı, çünkü herkes kendi hayatından sorumludur.",
            max_chars=mx,
        )
        if t.strip():
            st.markdown(argument.render(argument.analyze(t)))
    elif ss.adv == "Aporia Modu":
        name = st.selectbox("Filozof", ctx.registry.names)
        t = st.text_input("İddianı yaz", "Zenginlik mutluluk getirir.", max_chars=mx)
        if t.strip():
            st.markdown(modes.aporia(ctx.registry[name], t))
    elif ss.adv == "Felsefe Atölyesi":
        topic = st.text_input("Atölye konusu", "Adalet", max_chars=80)
        g, m = st.columns(2)
        st.markdown(
            library.workshop_plan(
                topic or "Felsefe",
                int(g.number_input("Grup sayısı", 2, 10, 4)),
                int(m.number_input("Süre (dk)", 20, 180, 60, step=5)),
            )
        )
    else:
        st.markdown("**Filozof künyeleri**")
        for name, prof in library.PROFILES.items():
            with st.expander(name):
                st.markdown(
                    f"**Dönem:** {prof['dönem']}\n\n**Yöntem:** {prof['yöntem']}\n\n**Kaynaklar:** {prof['kaynak']}"
                )
        st.markdown("**Kavramlar sözlüğü**")
        for term, text in library.GLOSSARY.items():
            st.markdown(f"- **{term}:** {text}")
        st.caption(
            "Tarihler ve eser adları kısa künyelerdir; ödev ve yayınlarda birincil kaynaktan doğrulayın."
        )


# ------------------------------------------------------------------ Ayarlar
def settings_page(ctx: Ctx) -> None:
    ss = st.session_state
    st.header("Ayarlar")
    st.subheader("Görünüm")
    ss.theme = (
        "Açık"
        if st.radio(
            "Tema",
            ["Koyu Tema", "Açık Tema"],
            index=1 if ss.theme == "Açık" else 0,
            horizontal=True,
        )
        == "Açık Tema"
        else "Koyu"
    )
    st.subheader("Ses")
    ss.voice_replies = st.toggle("Sesli yanıtları etkinleştir", value=ss.voice_replies)
    st.subheader("Dil")
    st.selectbox("Dil", ["Türkçe"], disabled=True, label_visibility="collapsed")
    st.subheader("Bildirimler")
    ss.reminders = st.toggle("Oturum hatırlatıcıları", value=ss.reminders)
    st.subheader("Motor ve gizlilik")
    st.write(f"**Motor:** {_provider(ctx).name}")
    ss.force_rule = st.toggle(
        "Yalnızca kural tabanlı (çevrimdışı) motoru kullan", value=ss.force_rule
    )
    if ctx.settings.uses_llm and st.button("Yerel LLM bağlantısını dene"):
        primary = getattr(ctx.provider, "primary", None)
        ok = primary is not None and primary.healthy()
        (st.success if ok else st.error)("Bağlantı başarılı." if ok else "Sunucuya ulaşılamadı.")
    st.markdown(
        f"- Sohbetler yalnızca oturumda (bellekte) tutulur; diske yazılmaz.\n- {ctx.settings.session_ttl_minutes} dakika işlem yapılmazsa otomatik silinir.\n- Kullanıcı metni log'lara yazılmaz."
    )
    if st.button("Tüm verilerimi şimdi sil", icon=":material/delete:"):
        retention.wipe(ss)
        st.toast("Oturum verileri silindi.")
    with st.expander("Etkin yapılandırma (sırsız)"):
        st.json(ctx.settings.public())


def sidebar_brand() -> None:
    H(
        f'<div class="brand">{theme.LOGO_SVG}<div><b>AGORA AI</b><small>DÜŞÜN · SORGULA · GELİŞTİR</small></div></div>'
    )
