import io
import logging

from config.logging_config import RedactingFilter, setup_logging
from safety.ratelimit import SlidingWindowLimiter
from services import pipeline


def _logger(name):
    buf = io.StringIO()
    handler = logging.StreamHandler(buf)
    handler.addFilter(RedactingFilter())
    log = logging.getLogger(name)
    log.handlers[:] = [handler]
    log.setLevel(logging.DEBUG)
    log.propagate = False
    return log, buf


def test_secrets_are_redacted_in_log_output():
    log, buf = _logger("agora.t1")
    log.info("key=%s header=Bearer abcdef123456", "sk-abcdefgh12345678")
    out = buf.getvalue()
    assert "abcdefgh1234" not in out and "abcdef123456" not in out and "[REDACTED]" in out


def test_setup_logging_is_idempotent_and_filtered():
    a, b = setup_logging("INFO"), setup_logging("DEBUG")
    assert a is b and len(a.handlers) == 1
    assert any(isinstance(f, RedactingFilter) for f in a.handlers[0].filters)


def test_user_text_never_logged_by_pipeline(caplog):
    secret_text = "benim çok özel sorum zebra-kelimesi"
    with caplog.at_level(logging.DEBUG, logger="agora"):
        lim = SlidingWindowLimiter(5, 60)
        pipeline.pre_process(secret_text, max_chars=200, limiter=lim)
        pipeline.pre_process(
            "kendimi öldürmek istiyorum zebra-kelimesi", max_chars=200, limiter=lim
        )
    assert "zebra" not in caplog.text
