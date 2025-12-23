import asyncio
import time
from pathlib import Path

from filelock import FileLock


class KoreaInvestmentSecuritiesDomesticStockInterProcessRateLimiter:
    MINIMUM_INTERVAL: float = 1

    def __init__(self,
                 lock_name: str = "binance_spot.lock"):
        base = Path.home() / ".binance_rate_limit"
        base.mkdir(parents=True, exist_ok=True)

        lock_file = base / lock_name
        timestamp_file = base / f"{lock_name}.ts"

        self._lock = FileLock(lock_file=str(lock_file))
        self._last_timestamp_file = timestamp_file

        if not self._last_timestamp_file.exists():
            self._last_timestamp_file.write_text("0.0")

        self._async_lock = asyncio.Lock()

    async def acquire(self):
        async with self._async_lock:
            await asyncio.to_thread(self._enter_lock)

    def _enter_lock(self):
        with self._lock:
            now = time.monotonic()

            try:
                last_timestamp = float(self._last_timestamp_file.read_text())
            except:
                last_timestamp = 0.0

            next_allowed = last_timestamp + self.MINIMUM_INTERVAL

            if next_allowed > now:
                time.sleep(next_allowed - now)

            self._last_timestamp_file.write_text(str(time.monotonic()))

    @classmethod
    def set_minimum_interval(cls, seconds: float):
        cls.MINIMUM_INTERVAL = seconds
