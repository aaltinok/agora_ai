# Mimari

```
app.py ─► ui ─► llm ─► services ─► philosophers / safety ─► config ─► utils
```
- **Akış:** kullanıcı metni → `services.pipeline` (temizle, kriz, hız sınırı, injection) → `llm` sağlayıcısı → akışlı yanıt.
- **Tek doğruluk kaynağı:** filozoflar `config/philosophers.yaml`'dadır; `philosophers/*.py` yalnızca karakter denetimi gibi özel mantık taşır.
- **Motor seçimi:** `llm/factory.py`. `rule` varsayılandır; `llm` seçilirse `FallbackProvider` hata anında kural motoruna düşer.
- **Soru bankası:** `services/qa_bank.py` ayrıştırır, Türkçe karakterlere duyarlı kök+benzerlik skoruyla eşleştirir, LLM için few-shot örnek seçer.
- **Test stratejisi:** birim (mantık), güvenlik (log/sır/ayar), katman (AST ile import kuralı), uygulama (Streamlit AppTest).

## Sokrates'le Yüz Yüze
`services/dialogue.py` saf bir durum makinesidir (aşamalar: `stance → reason → reflection → done`). Durum düz bir `dict`'tir (oturumda saklanır, TTL ile silinir). Serbest metin girişi olmadığından kriz/injection hattından geçmez; tüm girdi düğme seçimidir. Senaryo verisi `scripts/import_vr_draft.py` ile Word belgesinden üretilir.

## Sürüm 2 notları
- **Senaryolar:** `data/dialogues/*.json` (sokrates, aristoteles, farabi). Aristoteles ve Farabi kaynağı `scripts/authored_dialogues.py`; Sokrates Word taslağından. Aynı durum makinesi Python (`services/dialogue.py`) ve JS (`vr/src/dialogue.js`) olarak bulunur; parite testi ikisini karşılaştırır.
- **3B:** `vr/src/figures.js` (filozof iskeleti ve dönem giysileri), `citizens.js` (yurttaşlar: Yunan ve Abbasi stili), `props*.js` (dekor), `scenes.js` (üç mekân), `app.js` (arayüz, ses, VR).
- **Arayüz:** `ui/theme.py` (CSS), `ui/pages.py` (sayfalar), `ui/voice/` (sesli diyalog bileşeni), `ui/assets/` (portreler).
