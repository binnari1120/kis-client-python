import asyncio
import time

import pytest

from kis_client.domestic_stock.core.kis_domestic_stock_single_process_rate_limiter import \
    KoreaInvestmentSecuritiesDomesticStockSingleProcessRateLimiter
from kis_client.domestic_stock.kis_domestic_stock_client_factory import \
    KoreaInvestmentSecuritiesDomesticStockClientFactory


@pytest.mark.asyncio
async def test_single_process_rate_limiter_1():
    limiter = KoreaInvestmentSecuritiesDomesticStockSingleProcessRateLimiter()
    KoreaInvestmentSecuritiesDomesticStockSingleProcessRateLimiter.set_minimum_interval(seconds=2)

    timestamp_queue = asyncio.Queue()

    async def worker():
        await limiter.acquire()
        timestamp = time.monotonic()
        await timestamp_queue.put(timestamp)

    tasks = [asyncio.create_task(worker()) for _ in range(10)]
    await asyncio.gather(*tasks)

    timestamps = []
    while not timestamp_queue.empty():
        timestamps.append(await timestamp_queue.get())

    timestamps.sort()

    print("==== Single-Process Test Result ====")
    for i, timestamp in enumerate(timestamps):
        print(f"{i}: {timestamp}")

    for i in range(1, len(timestamps)):
        interval = timestamps[i] - timestamps[i - 1]
        print(f"Interval {i}: {interval:.3f}s")

        assert interval >= 1.0 - 0.05


@pytest.mark.asyncio
async def test_single_process_rate_limiter_2():
    factory = KoreaInvestmentSecuritiesDomesticStockClientFactory()
    client = factory.create_client(use_single_process_rate_limiter=True,
                                   use_inter_process_rate_limiter=False)

    timestamp_queue = asyncio.Queue()

    async def worker():
        await client.rest_client.get_ticker_price_v3_async()
        KoreaInvestmentSecuritiesDomesticStockSingleProcessRateLimiter.set_minimum_interval(seconds=2)

        timestamp = time.time()
        await timestamp_queue.put(timestamp)

    tasks = [asyncio.create_task(worker()) for _ in range(10)]
    await asyncio.gather(*tasks)

    timestamps = []
    while not timestamp_queue.empty():
        timestamps.append(await timestamp_queue.get())

    timestamps.sort()

    print("==== Single-Process Test Result ====")
    for i, timestamp in enumerate(timestamps):
        print(f"{i}: {timestamp}")

    for i in range(1, len(timestamps)):
        interval = timestamps[i] - timestamps[i - 1]
        print(f"Interval {i}: {interval:.3f}s")

        assert interval >= 1.0 - 0.2
