import asyncio
import time


class KoreaInvestmentSecuritiesDomesticStockSingleProcessRateLimiter:
    MINIMUM_INTERVAL: float = 0.1

    def __init__(self):
        self._lock = asyncio.Lock()
        self._last_timestamp = 0.0

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            next_allowed = self._last_timestamp + self.MINIMUM_INTERVAL

            if next_allowed > now:
                await asyncio.sleep(next_allowed - now)

            self._last_timestamp = time.monotonic()

    @classmethod
    def set_minimum_interval(cls, seconds: float):
        cls.MINIMUM_INTERVAL = seconds
