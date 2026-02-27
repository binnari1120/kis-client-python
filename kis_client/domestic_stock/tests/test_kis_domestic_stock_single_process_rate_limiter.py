import asyncio
import pathlib
import time

import pytest
import yaml

from kis_client.domestic_stock.core.kis_domestic_stock_single_process_rate_limiter import \
    KoreaInvestmentSecuritiesDomesticStockSingleProcessRateLimiter
from kis_client.domestic_stock.enums.kis_domestic_stock_fid_cond_mrkt_div_code import \
    KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode
from kis_client.domestic_stock.kis_domestic_stock_client_factory import \
    KoreaInvestmentSecuritiesDomesticStockClientFactory
from kis_client.domestic_stock.models.kis_domestic_stock_credentials import \
    KoreaInvestmentSecuritiesDomesticStockCredentials

factory = KoreaInvestmentSecuritiesDomesticStockClientFactory()
client = factory.create_client()


@pytest.mark.asyncio
async def test_set_credentials():
    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml", "r",
              encoding="utf-8") as file:
        accounts = yaml.safe_load(file)

    account = accounts["Spot"]
    public_key = account.get("public_key", "")
    private_key = account.get("private_key", "")
    if not public_key:
        raise Exception("Empty value: public_key")
    elif not private_key:
        raise Exception("Empty value: private_key")

    credentials = KoreaInvestmentSecuritiesDomesticStockCredentials(public_key=accounts["Spot"]["public_key"],
                                                                    private_key=accounts["Spot"]["private_key"])
    await client.set_credentials_async(credentials=credentials)


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


with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
    accounts = yaml.safe_load(file)
credentials = KoreaInvestmentSecuritiesDomesticStockCredentials(public_key=accounts["Spot"]["public_key"],
                                                                private_key=accounts["Spot"]["private_key"])


@pytest.mark.asyncio
async def test_single_process_rate_limiter_2():
    timestamp_queue = asyncio.Queue()

    async def worker():
        code = KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode.UN
        iscd = "005930"

        price_details = await client.rest_client.get_quotations_price_2_v1_async(fid_cond_mrkt_div_code=code,
                                                                                 fid_input_iscd=iscd)
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
