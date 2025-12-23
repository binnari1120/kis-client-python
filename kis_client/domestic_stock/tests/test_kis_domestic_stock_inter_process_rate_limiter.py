import asyncio
import multiprocessing
import os
import pathlib
import time

import pytest
import yaml

from kis_client.domestic_stock.core.kis_domestic_stock_inter_process_rate_limiter import \
    KoreaInvestmentSecuritiesDomesticStockInterProcessRateLimiter
from kis_client.domestic_stock.kis_domestic_stock_client_factory import KoreaInvestmentSecuritiesDomesticStockClientFactory
from kis_client.domestic_stock.models.kis_domestic_stock_credentials import \
    KoreaInvestmentSecuritiesDomesticStockCredentials


def worker_process(use_queue: multiprocessing.Queue):
    async def _run():
        limiter = KoreaInvestmentSecuritiesDomesticStockInterProcessRateLimiter()
        KoreaInvestmentSecuritiesDomesticStockInterProcessRateLimiter.set_minimum_interval(seconds=2)

        for _ in range(10):
            await limiter.acquire()

            timestamp = time.monotonic()
            pid = os.getpid()
            # print(result)
            use_queue.put((pid, timestamp))

    asyncio.run(_run())


with open(f"{pathlib.Path(__file__).parent.parent.parent.parent}/configurations/accounts.yaml") as file:
    accounts = yaml.safe_load(file)
credentials = KoreaInvestmentSecuritiesDomesticStockCredentials(public_key=accounts["Spot"]["public_key"],
                                                                private_key=accounts["Spot"]["private_key"])


def worker_process_2(use_queue: multiprocessing.Queue):
    async def _run():
        factory = KoreaInvestmentSecuritiesDomesticStockClientFactory()
        client = factory.create_client(use_single_process_rate_limiter=False,
                                       use_inter_process_rate_limiter=True)
        client.private_rest_client.set_credentials(credentials=credentials)
        KoreaInvestmentSecuritiesDomesticStockInterProcessRateLimiter.set_minimum_interval(seconds=2)

        for _ in range(10):
            result = await client.private_rest_client.get_account_v3_async()

            now = time.monotonic()
            pid = os.getpid()
            # print(result)
            use_queue.put((pid, now))

    asyncio.run(_run())


@pytest.mark.asyncio
async def test_inter_process_rate_limiter_1():
    queue = multiprocessing.Queue()

    process_1 = multiprocessing.Process(target=worker_process, args=(queue,))
    process_2 = multiprocessing.Process(target=worker_process, args=(queue,))

    process_1.start()
    process_2.start()

    process_1.join()
    process_2.join()

    results = []
    while not queue.empty():
        results.append(queue.get())

    results.sort(key=lambda x: x[1])

    print("==== Inter-Process Test Result ====")
    for pid, timestamp in results:
        print(f"PID={pid}, time={timestamp}")

    for i in range(1, len(results)):
        interval = results[i][1] - results[i - 1][1]
        print(f"Interval: {interval:.3f}s")

        assert interval >= 1.0 - 0.05


@pytest.mark.asyncio
async def test_inter_process_rate_limiter_2():
    queue = multiprocessing.Queue()

    process_1 = multiprocessing.Process(target=worker_process_2, args=(queue,))
    process_2 = multiprocessing.Process(target=worker_process_2, args=(queue,))

    process_1.start()
    process_2.start()

    process_1.join()
    process_2.join()

    results = []
    while not queue.empty():
        results.append(queue.get())

    results.sort(key=lambda x: x[1])

    print("==== Inter-Process Test Result ====")
    for pid, timestamp in results:
        print(f"PID={pid}, time={timestamp}")

    for i in range(1, len(results)):
        interval = results[i][1] - results[i - 1][1]
        print(f"Interval: {interval:.3f}s")

        assert interval >= 1.0 - 0.4
