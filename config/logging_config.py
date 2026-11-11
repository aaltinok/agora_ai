"""Log yapılandırması. İlke: kullanıcı metni ve sırlar ASLA loglanmaz."""

from __future__ import annotations

import logging

from utils.secrets import redact

LOGGER_NAME = "agora"
_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


class RedactingFilter(logging.Filter):
    """Her kaydı yazılmadan önce sır desenlerinden arındırır."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact(record.getMessage())
        record.args = ()
        return True


def setup_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level.upper())
    if not getattr(logger, "_agora_configured", False):
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_FORMAT))
        handler.addFilter(RedactingFilter())
        logger.addHandler(handler)
        logger.propagate = False
        logger._agora_configured = True  # type: ignore[attr-defined]
    return logger
