# Değişiklik Günlüğü

## [2.0.0] — 2026-11-09
### Değişti
- Montaigne yerine **Farabi**. Filozof alanı `emoji` yerine `accent` renk; portreler 3B modellerden üretilir.
- 3B: üç senaryo (Atina Agorası, Lykeion, Abbasi ilim meclisi), dönemine uygun giysi ve mimari (Dor düzeni, sivri kemer vb.).
- Diyalog: konu başına 6 soru, 6 gerekçe seçeneği, 6 köprü cümlesi; Aristoteles ve Farabi senaryoları eklendi.
- Arayüz ekran görüntüsündeki tasarıma yaklaştırıldı: tema, sol menü, portre kartları, balon sohbet, oturum özeti, ayarlar.
- Emoji kullanımı kaldırıldı (test ile korunur).
### Eklendi
- Sesli Diyalog sayfası (Streamlit bileşeni), PDF dışa aktarma, Felsefe Atölyesi ve Kütüphane.

## [1.2.1] — 2026-10-24
### Değişti
- 3B Agora yenilendi: uzuvlu ve animasyonlu insanlar (yürüyen, konuşan, oturan, satıcı), boyalı frizli stoa, meander döşeme, çeşme, heykel, pazar tezgâhı, gölge, bulut, kuş, uzak şehir; `?lite` modu.

## [1.2.0] — 2026-10-23
### Eklendi
- 3B Agora (WebXR): prosedürel Sokrates, Türkçe TTS/STT, VR paneli, tek dosya çevrimdışı derleme (`scripts/build_vr.py`).
- JS ↔ Python diyalog motoru parite testi.
### Değişti (VR taslağındaki "konuşma kurallarına" göre)
- Sokrates: önce açık cevap, karşı soruyla bitiş, hemen doğru/yanlış demez, "bilmiyorum"da daha basit örnek, aynı karşı soru tekrarlanmaz, konuşma sonunda düşünmeye devam hatırlatması.
- Öğrencinin seçebileceği 7 soru (sohbette düğme) ve "Konuşmayı bitir".

## [1.1.0] — 2026-10-22
### Eklendi
- "Sokrates'le Yüz Yüze" sayfası ve `services/dialogue.py` diyalog durum makinesi (VR taslağından).
- `scripts/import_vr_draft.py`: Word taslağı → diyalog JSON + soru-cevap bankası.
- Soru bankası birden çok dosyayı birleştirebiliyor (`QABank.from_files`).

## [1.0.0] — 2026-10-11
### Eklendi
- Streamlit arayüzü: Ana Sayfa, Sohbet, Filozoflar, Karşılaştır, Soru Bankası, Oturumlar, İleri Düzey, Ayarlar.
- API'siz kural tabanlı motor (soru bankası eşleştirme + filozof şablonları + mod çözümleyicileri).
- İsteğe bağlı ücretsiz yerel LLM (Ollama / LM Studio, OpenAI uyumlu) ve otomatik geri düşüş.
- Güvenlik katmanı: kriz tespiti, girdi temizleme, injection sezgisi, hız sınırı, sır maskeleme.
- Veri saklama: yalnızca bellek, TTL ile silme, tek tıkla temizleme.
- CI: test, lint, güvenlik (pip-audit, bandit, gitleaks).
