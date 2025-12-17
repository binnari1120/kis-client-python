import pathlib
from datetime import datetime, timezone, timedelta
from typing import Any

import pytest
import yaml

from kis_client.domestic_spot.enums.kis_domestic_spot_fid_cond_mrkt_div_code import \
    KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode
from kis_client.domestic_spot.kis_domestic_spot_client_factory import KoreaInvestmentSecuritiesSpotClientFactory
from kis_client.domestic_spot.models.kis_domestic_spot_credentials import \
    KoreaInvestmentSecuritiesDomesticSpotCredentials

factory = KoreaInvestmentSecuritiesSpotClientFactory()
client = factory.create_client()


# @pytest.mark.asyncio
# async def test_ensure_credentials():
#     with pytest.raises(ValueError):
#         await client.private_rest_client.get_account_v3_async()


def _is_expired(expiration: str) -> bool:
    if not expiration:
        return True
    tz_info = timezone(timedelta(hours=9))
    current_kst_date = datetime.now().replace(tzinfo=tz_info)
    expiration_date = datetime.fromisoformat(expiration)
    if expiration_date.tzinfo is None:
        expiration_date = expiration_date.replace(tzinfo=tz_info)
    return expiration_date <= current_kst_date


def _save(accounts: Any):
    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml", "w",
              encoding="utf-8") as file:
        accounts = yaml.safe_dump(accounts, file, allow_unicode=True)


def _set_access_token():
    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml", "r",
              encoding="utf-8") as file:
        accounts = yaml.safe_load(file)
    account = accounts["Spot"]
    public_key = account.get("public_key", "")
    private_key = account.get("private_key", "")
    if (not public_key) or (not private_key):
        raise Exception("")
    access_token = account.get("access_token", "")
    client.set_access_token(access_token=access_token)
    client.set_access_token(access_token=access_token)


@pytest.mark.asyncio
async def test_set_credentials():
    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml", "r",
              encoding="utf-8") as file:
        accounts = yaml.safe_load(file)

    account = accounts["Spot"]
    public_key = account.get("public_key", "")
    private_key = account.get("private_key", "")
    if (not public_key) or (not private_key):
        raise Exception("")

    access_token = account.get("access_token", "")
    access_token_expiration = account.get("access_token_expiration", "")

    if (not access_token) or _is_expired(expiration=access_token_expiration):
        print("토큰 없음 → 신규 발급 중 ...")
        credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                       private_key=accounts["Spot"]["private_key"])
        client.set_credentials(credentials=credentials)
        token_details = await client.public_rest_client.get_token_async()
        # print(token_details)
        access_token = token_details["access_token"]
        access_token_expiration = token_details["access_token_token_expired"]

        account["access_token"] = access_token
        account["access_token_expiration"] = access_token_expiration

        _save(accounts)


@pytest.mark.asyncio
async def test_get_price_v1_async():
    _set_access_token()

    code = KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode.UN
    iscd = "005930"

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"])
    client.set_credentials(credentials=credentials)

    price_details = await client.public_rest_client.get_quotations_price_v1_async(fid_cond_mrkt_div_code=code,
                                                                                  fid_input_iscd=iscd)
    print(price_details)
    assert "output" in price_details
    assert "msg1" in price_details and price_details["msg1"] == "정상처리 되었습니다."


@pytest.mark.asyncio
async def test_get_price_2_v1_async():
    _set_access_token()

    code = KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode.UN
    iscd = "005930"

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"])
    client.set_credentials(credentials=credentials)

    price_details = await client.public_rest_client.get_quotations_price_2_v1_async(fid_cond_mrkt_div_code=code,
                                                                                    fid_input_iscd=iscd)
    print(price_details)
    assert "output" in price_details
    assert "msg1" in price_details and price_details["msg1"] == "정상처리 되었습니다."


@pytest.mark.asyncio
async def test_get_ccnl_v1_async():
    _set_access_token()

    code = KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode.UN
    iscd = "005930"

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"])
    client.set_credentials(credentials=credentials)

    price_details = await client.public_rest_client.get_quotations_ccnl_v1_async(fid_cond_mrkt_div_code=code,
                                                                                 fid_input_iscd=iscd)
    print(price_details)
    assert "output" in price_details
    assert "msg1" in price_details and price_details["msg1"] == "정상처리 되었습니다."


@pytest.mark.asyncio
async def test_get_quotations_inquire_time_itemchartprice_v1_async():
    _set_access_token()

    code = KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode.UN
    iscd = "005930"

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"])
    client.set_credentials(credentials=credentials)

    chart_price_details = await client.public_rest_client.get_quotations_inquire_time_itemchartprice_v1_async(
        fid_cond_mrkt_div_code=code,
        fid_input_iscd=iscd,
        fid_input_hour_1="090000",
        fid_pw_data_incu_yn="1",
        fid_etc_cls_code="")
    print(chart_price_details)
    print(chart_price_details["output1"])
    print(chart_price_details["output2"])
    print("==========")

    assert "msg1" in chart_price_details and chart_price_details["msg1"] == "정상처리 되었습니다."


@pytest.mark.asyncio
async def test_get_quotations_inquire_time_dailychartprice_v1_async():
    _set_access_token()

    code = KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode.UN
    iscd = "005930"

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"])
    client.set_credentials(credentials=credentials)

    chart_price_details = await client.public_rest_client.get_quotations_inquire_time_dailychartprice_v1_async(
        fid_cond_mrkt_div_code=code,
        fid_input_iscd=iscd,
        fid_input_hour_1="090000",
        fid_pw_data_incu_yn="1",
        fid_input_date_1="20241023",
        fid_etc_cls_code="")
    print(chart_price_details)
    print(chart_price_details["output1"])
    print(chart_price_details["output2"])
    print("==========")

    assert "msg1" in chart_price_details and chart_price_details["msg1"] == "정상처리 되었습니다."
