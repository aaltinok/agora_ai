# Katman bağımlılıkları

| Katman | Paket | İçe aktarabilir |
|---|---|---|
| 0 | `utils` | — |
| 1 | `config` | utils |
| 2 | `philosophers`, `safety` | utils, config (birbirini içe aktarmaz) |
| 3 | `services` | 0–2 |
| 4 | `llm` | 0–3 |
| 5 | `ui` | 0–4 |
| — | `app.py` | hepsi |

Kural: bir paket yalnızca **kendinden alt** katmanı içe aktarır. `tests/unit/test_layer_dependencies.py` bunu AST ile denetler ve CI'da çalışır. Bu sayede `services` mantığı Streamlit'siz test edilebilir ve sağlayıcılar kolayca değiştirilebilir.
