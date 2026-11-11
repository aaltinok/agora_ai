# Katkı Rehberi

1. `pip install -r requirements-dev.txt && pre-commit install`
2. Değişiklikten önce ve sonra `pytest` ve `ruff check . && ruff format .` çalıştırın.
3. Katman kuralına uyun (`docs/layer_dependencies.md`); `tests/unit/test_layer_dependencies.py` ihlali yakalar.
4. Yeni filozof: `config/philosophers.yaml`'a ekleyin (şablonlarda yalnızca `{kw}`, `{claim}`), gerekiyorsa `philosophers/` altına özel sınıf yazıp `registry.py`'ye bağlayın, banka dosyasına soru ekleyin.
5. `data/` altına dosya eklerken `LICENSE_MATRIX.md`'yi güncelleyin.
6. Sır, API anahtarı, kişisel veri commit etmeyin. Kullanıcı metnini loglamayın.
7. Davranış değiştiren her PR test içermelidir; `CHANGELOG.md`'ye satır ekleyin.
