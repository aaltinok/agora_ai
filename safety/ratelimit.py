"""Oturum başına kayan pencere hız sınırlayıcı."""

from __future__ import annotations

import time
from collections import deque
from collections.abc import Callable


class SlidingWindowLimiter:
    def __init__(
        self, max_events: int, window_s: float = 60.0, clock: Callable[[], float] = time.monotonic
    ):
        if max_events < 1 or window_s <= 0:
            raise ValueError("max_events >= 1 ve window_s > 0 olmalı.")
        self.max_events, self.window_s, self._clock = max_events, window_s, clock
        self._events: deque[float] = deque()

    def _evict(self, now: float) -> None:
        while self._events and now - self._events[0] >= self.window_s:
            self._events.popleft()

    def allow(self) -> bool:
        """Olay serbestse kaydeder ve True döner."""
        now = self._clock()
        self._evict(now)
        if len(self._events) >= self.max_events:
            return False
        self._events.append(now)
        return True

    def retry_after(self) -> int:
        now = self._clock()
        self._evict(now)
        if len(self._events) < self.max_events:
            return 0
        return max(1, int(self.window_s - (now - self._events[0])) + 1)
