# AGORA AI

Filozoflarla diyalog kuran Streamlit uygulaması: **Sokrates, Platon, Aristoteles, Epiktetos ve Farabi**.
API anahtarı, hesap ya da internet gerektirmez; isterseniz ücretsiz yerel bir modelle (Ollama) zenginleştirilir.

## Hızlı başlangıç
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Sayfalar (ekran görüntüsündeki tasarıma göre)
Ana Sayfa, Sohbet (balonlu diyalog), Filozoflar (keşfet), Karşılaştır (5 sütun), Oturumlar (özet, not, **PDF indir**, paylaş),
Sesli Diyalog (Türkçe ses tanıma ve okuma), Yüz Yüze (dallanan senaryolu diyalog), 3B Agora, Soru Bankası, İleri Düzey
(soru analizörü, argüman değerlendirme, aporia modu, felsefe atölyesi, kütüphane), Ayarlar (koyu/açık tema, sesli yanıt, hatırlatıcı).

## Üç 3B senaryo (`vr/`)
| Filozof | Mekân | Dönem |
|---|---|---|
| Sokrates | Atina Agorası: Dor düzeninde stoalar, toprak zemin, tholos, herm direkleri, çınarlar, uzakta Akropolis | MÖ 5. yüzyıl |
| Aristoteles | Lykeion: örtülü yürüyüş yolu (peripatos), çınar koruluğu, papirüs rulo dolabı | MÖ 4. yüzyıl |
| Farabi | Abbasi dönemi ilim meclisi: sivri kemerli revak, iwan, havuz, hurma, rahle, usturlap, ud | 10. yüzyıl |

Her senaryoda **5 konu, konu başına 6 soru**; her soruda Evet/Hayır/Kararsızım dalı, ardından **6 gerekçe seçeneği**.
Mekân ve giysiler dönem bilgisine dayanan yaklaşık canlandırmalardır; belgelenmiş portre veya görüntü değildir.
Tek dosya, çevrimdışı: `vr/dist/agora_vr.html`. Ayrıntı, sınırlar ve gizlilik: `vr/README.md`.

## Motorlar
| Motor | Gereksinim | Ne yapar |
|---|---|---|
| `rule` (varsayılan) | yok | Soru bankasından en yakın cevabı verir; yoksa filozofun şablonuyla yeni soru kurar. |
| `llm` | [Ollama](https://ollama.com) vb. | Serbest sohbet. `ollama pull qwen2.5:7b`, `.env` içinde `AGORA_ENGINE=llm`. Hata olursa otomatik `rule`'a düşer. |

Yapılandırma: `cp .env.example .env`. Sırlar `.env` veya `.streamlit/secrets.toml`'da durur (gitignore'da).

## İçerik kaynakları ve doğruluk
- `scripts/authored_dialogues.py`: Aristoteles ve Farabi senaryolarının kaynak metni. Metinler Nikomakhos'a Etik, Politika, Organon ve
  Farabi'nin Erdemli Şehir, İlimlerin Sayımı, Mutluluğa Ulaşma ve Büyük Müzik Kitabı gibi eserlerindeki başlıca görüşlere dayanır;
  **taslaktır, tarihsel ve felsefi doğruluk için bir uzman tarafından gözden geçirilmelidir.**
- `data/texts/qa_bank.md` içinde yalnızca örnekler vardır; 150 soruluk dosyanızla değiştirin (Montaigne kayıtları yok sayılır).
- Sokrates senaryosu Word taslağından üretilir: `python scripts/import_vr_draft.py "taslak.docx"`; ardından `python scripts/build_dialogues.py`.

## Geliştirme
```bash
pip install -r requirements-dev.txt && pre-commit install && pytest
python scripts/build_dialogues.py      # senaryo JSON'ları
python scripts/build_vr.py             # 3B sayfa
python -m scripts.render_portraits     # portreler ve ana sayfa görseli (Playwright gerekir)
```
Mimari: `docs/architecture.md`.

## Sınırlar
Persona'lar simülasyondur; yanıtlar kaynak yerine geçmez. Agora AI bir kriz hizmeti veya tıbbi/hukuki danışman değildir.
Lisans: kod MIT, içerik CC BY-SA 4.0 (`LICENSE-CONTENT.md`). Portre ve mekân görselleri bu projenin 3B modellerinden üretilmiştir.
