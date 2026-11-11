from ui import assets, theme


def test_portraits_and_hero_exist_for_every_philosopher(registry):
    for p in registry:
        assert assets.portrait(p.key).startswith("data:image/png;base64,"), p.key
    assert assets.hero().startswith("data:image/jpeg;base64,")


def test_theme_variants():
    assert "#0b1730" in theme.css("Koyu") and "#f3f6ff" in theme.css("Açık")
