# Veri saklama ve gizlilik

| Veri | Nerede | Ne kadar | Silme |
|---|---|---|---|
| Sohbet, not, özet, Yüz Yüze seçimleri | Yalnızca tarayıcı oturumu (sunucu belleği) | `AGORA_SESSION_TTL_MIN` dk hareketsizlikten sonra silinir | Ayarlar → "Tüm verilerimi şimdi sil" |
| Kriz mesajları | Oturumda işaretlenir (`kind=safety`) | Aynı TTL | Dışa aktarma, özet ve modele gönderimden **hariç** tutulur |
| Dışa aktarılan dosya | Kullanıcının cihazı | Kullanıcı kontrolünde | — |
| Log | stderr | Platforma bağlı | **Kullanıcı metni asla yazılmaz**; sırlar maskelenir |
| Sırlar | `.env` / `secrets.toml` | — | Repoya girmez (gitignore + test) |

- Diske, veritabanına veya üçüncü tarafa varsayılan olarak hiçbir şey yazılmaz/gönderilmez.
- `llm` motorunda mesajlar yalnızca yapılandırdığınız sunucuya gider; uzak sunucuda https zorunludur ve o servisin gizlilik politikası geçerlidir.
- Çok kullanıcılı bir dağıtım yapacaksanız KVKK kapsamında aydınlatma metni ve saklama süresi kararı alıp bu belgeyi güncelleyin.
