import pathlib

import pytest
import yaml

from kis_client.domestic_stock.enums.kis_domestic_stock_fid_cond_mrkt_div_code import \
    KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode
from kis_client.domestic_stock.enums.kis_domestic_stock_fid_period_div_cd import \
    KoreaInvestmentSecuritiesDomesticStockFidPeriodDivCd
from kis_client.domestic_stock.kis_domestic_stock_client_factory import \
    KoreaInvestmentSecuritiesDomesticStockClientFactory
from kis_client.domestic_stock.models.kis_domestic_stock_credentials import \
    KoreaInvestmentSecuritiesDomesticStockCredentials

factory = KoreaInvestmentSecuritiesDomesticStockClientFactory()
client = factory.create_client()


# @pytest.mark.asyncio
# async def test_ensure_credentials():
#     with pytest.raises(ValueError):
#         await client.private_rest_client.get_account_v3_async()

#
# def _is_expired(expiration: str) -> bool:
#     if not expiration:
#         return True
#     tz_info = timezone(timedelta(hours=9))
#     current_kst_date = datetime.now().replace(tzinfo=tz_info)
#     expiration_date = datetime.fromisoformat(expiration)
#     if expiration_date.tzinfo is None:
#         expiration_date = expiration_date.replace(tzinfo=tz_info)
#     return expiration_date <= current_kst_date
#
#
# def _save(accounts: Any):
#     with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml", "w",
#               encoding="utf-8") as file:
#         accounts = yaml.safe_dump(accounts, file, allow_unicode=True)
#
#
# def _set_access_token():
#     with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml", "r",
#               encoding="utf-8") as file:
#         accounts = yaml.safe_load(file)
#     account = accounts["Spot"]
#     public_key = account.get("public_key", "")
#     private_key = account.get("private_key", "")
#     if (not public_key) or (not private_key):
#         raise Exception("")
#     access_token = account.get("access_token", "")
#     client.set_access_token(access_token=access_token)
#     client.set_access_token(access_token=access_token)


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
async def test_get_quotations_price_v1_async():
    code = KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode.UN
    iscd = "005930"

    return
    price_details = await client.rest_client.get_quotations_price_v1_async(fid_cond_mrkt_div_code=code,
                                                                           fid_input_iscd=iscd)
    print(f"========== test_get_quotations_price_v1_async ==========")
    print(price_details)

    assert "output" in price_details
    assert "msg1" in price_details and price_details["msg1"] == "정상처리 되었습니다."


@pytest.mark.asyncio
async def test_get_quotations_price_2_v1_async():
    code = KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode.UN
    iscd = "005930"

    price_details = await client.rest_client.get_quotations_price_2_v1_async(fid_cond_mrkt_div_code=code,
                                                                             fid_input_iscd=iscd)
    print(f"========== test_get_quotations_price_2_v1_async ==========")
    print(price_details)

    assert "output" in price_details
    assert "msg1" in price_details and price_details["msg1"] == "정상처리 되었습니다."


@pytest.mark.asyncio
async def test_get_quotations_inquire_ccnl_v1_async():
    code = KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode.UN
    iscd = "005930"

    price_details = await client.rest_client.get_quotations_inquire_ccnl_v1_async(fid_cond_mrkt_div_code=code,
                                                                                  fid_input_iscd=iscd)
    return
    print(f"========== test_get_quotations_inquire_ccnl_v1_async ==========")
    print(price_details)

    assert "output" in price_details
    assert "msg1" in price_details and price_details["msg1"] == "정상처리 되었습니다."


@pytest.mark.asyncio
async def test_get_quotations_inquire_daily_price_v1_async():
    code = KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode.UN
    iscd = "005930"

    chart_price_details = await client.rest_client.get_quotations_inquire_daily_price_v1_async(
        fid_cond_mrkt_div_code=code,
        fid_input_iscd=iscd,
        fid_period_div_code=KoreaInvestmentSecuritiesDomesticStockFidPeriodDivCd.M,
        fid_org_adj_prc="1")

    print(f"========== test_get_quotations_inquire_daily_price_v1_async ==========")
    print(chart_price_details)

    assert "msg1" in chart_price_details and chart_price_details["msg1"] == "정상처리 되었습니다."


@pytest.mark.asyncio
async def test_get_quotations_inquire_time_itemchartprice_v1_async():
    code = KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode.UN
    iscd = "005930"

    return
    chart_price_details = await client.rest_client.get_quotations_inquire_time_itemchartprice_v1_async(
        fid_cond_mrkt_div_code=code,
        fid_input_iscd=iscd,
        fid_input_hour_1="090000",
        fid_pw_data_incu_yn="1",
        fid_etc_cls_code="")

    print(f"========== test_get_quotations_inquire_time_itemchartprice_v1_async ==========")
    print(chart_price_details)

    assert "msg1" in chart_price_details and chart_price_details["msg1"] == "정상처리 되었습니다."


@pytest.mark.asyncio
async def test_get_quotations_inquire_time_dailychartprice_v1_async():
    code = KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode.UN
    iscd = "005930"

    return
    chart_price_details = await client.rest_client.get_quotations_inquire_time_dailychartprice_v1_async(
        fid_cond_mrkt_div_code=code,
        fid_input_iscd=iscd,
        fid_input_hour_1="090000",
        fid_pw_data_incu_yn="1",
        fid_input_date_1="20241023",
        fid_etc_cls_code="")

    print(f"========== test_get_quotations_inquire_time_dailychartprice_v1_async ==========")
    print(chart_price_details)

    assert "msg1" in chart_price_details and chart_price_details["msg1"] == "정상처리 되었습니다."
