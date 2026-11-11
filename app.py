"""AGORA AI: filozoflarla diyalog.   Çalıştırma:  streamlit run app.py"""

import streamlit as st

from config.constants import APP_NAME, APP_VERSION
from config.logging_config import setup_logging
from config.paths import DIALOGUE_DIR, QA_BANK_PATH, QA_VR_PATH
from config.settings import SettingsError, get_settings
from llm.factory import build_provider
from llm.rule_based import RuleBasedProvider
from philosophers.registry import get_registry
from services import dialogue, retention
from services.qa_bank import QABank
from ui import pages, theme
from ui.state import NAV, PAGES, init_state

st.set_page_config(
    page_title=APP_NAME,
    page_icon=str(pages.assets.ASSETS / "portraits" / "sokrates.png"),
    layout="wide",
)


@st.cache_resource
def resources() -> pages.Ctx:
    settings = get_settings()
    setup_logging(settings.log_level)
    registry = get_registry()
    bank = QABank.from_files([QA_BANK_PATH, QA_VR_PATH], known=set(registry.names))
    scripts = dialogue.load_scripts(DIALOGUE_DIR)
    return pages.Ctx(
        settings, registry, bank, build_provider(settings, bank), RuleBasedProvider(bank), scripts
    )


try:
    ctx = resources()
except SettingsError as exc:
    st.error(f"Yapılandırma hatası: {exc}")
    st.stop()

ss = st.session_state
init_state(ss, ctx.settings, ctx.registry.names[0])
if retention.purge_if_expired(ss, ctx.settings.session_ttl_minutes * 60):
    st.toast("Hareketsizlik nedeniyle oturum verileri silindi.")
retention.touch(ss)
st.markdown(theme.css(ss.theme), unsafe_allow_html=True)

with st.sidebar:
    pages.sidebar_brand()
    st.write("")
    for label, icon in NAV:
        st.button(
            label,
            key=f"nav_{label}",
            icon=f":material/{icon}:",
            on_click=pages.go,
            args=(label,),
            type="primary" if ss.page == label else "secondary",
            width="stretch",
        )
    st.caption(f"Motor: {pages._provider(ctx).name}")
    st.caption(f"v{APP_VERSION}")

if ss.page not in PAGES:
    ss.page = PAGES[0]
{
    "Ana Sayfa": pages.home,
    "Sohbet": pages.chat,
    "Filozoflar": pages.philosophers,
    "Karşılaştır": pages.compare,
    "Oturumlar": pages.sessions,
    "Sesli Diyalog": pages.voice_page,
    "Yüz Yüze": pages.face_to_face,
    "3B Agora": pages.vr_agora,
    "Soru Bankası": pages.question_bank,
    "İleri Düzey": pages.advanced,
    "Ayarlar": pages.settings_page,
}[ss.page](ctx)
