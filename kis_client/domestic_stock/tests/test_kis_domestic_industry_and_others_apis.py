import pathlib

import pytest
import yaml

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
async def test_get_quotations_chk_holiday_v1_async():
    # {
    #     "ctx_area_nk": "20260128            ",
    #     "ctx_area_fk": "20260105            ",
    #     "output": [
    #         {
    #             "bass_dt": "20260105",
    #             "wday_dvsn_cd": "02",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260106",
    #             "wday_dvsn_cd": "03",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260107",
    #             "wday_dvsn_cd": "04",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260108",
    #             "wday_dvsn_cd": "05",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260109",
    #             "wday_dvsn_cd": "06",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260110",
    #             "wday_dvsn_cd": "07",
    #             "bzdy_yn": "N",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "N",
    #             "sttl_day_yn": "N"
    #         },
    #         {
    #             "bass_dt": "20260111",
    #             "wday_dvsn_cd": "01",
    #             "bzdy_yn": "N",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "N",
    #             "sttl_day_yn": "N"
    #         },
    #         {
    #             "bass_dt": "20260112",
    #             "wday_dvsn_cd": "02",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260113",
    #             "wday_dvsn_cd": "03",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260114",
    #             "wday_dvsn_cd": "04",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260115",
    #             "wday_dvsn_cd": "05",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260116",
    #             "wday_dvsn_cd": "06",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260117",
    #             "wday_dvsn_cd": "07",
    #             "bzdy_yn": "N",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "N",
    #             "sttl_day_yn": "N"
    #         },
    #         {
    #             "bass_dt": "20260118",
    #             "wday_dvsn_cd": "01",
    #             "bzdy_yn": "N",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "N",
    #             "sttl_day_yn": "N"
    #         },
    #         {
    #             "bass_dt": "20260119",
    #             "wday_dvsn_cd": "02",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260120",
    #             "wday_dvsn_cd": "03",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260121",
    #             "wday_dvsn_cd": "04",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260122",
    #             "wday_dvsn_cd": "05",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260123",
    #             "wday_dvsn_cd": "06",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260124",
    #             "wday_dvsn_cd": "07",
    #             "bzdy_yn": "N",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "N",
    #             "sttl_day_yn": "N"
    #         },
    #         {
    #             "bass_dt": "20260125",
    #             "wday_dvsn_cd": "01",
    #             "bzdy_yn": "N",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "N",
    #             "sttl_day_yn": "N"
    #         },
    #         {
    #             "bass_dt": "20260126",
    #             "wday_dvsn_cd": "02",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260127",
    #             "wday_dvsn_cd": "03",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         },
    #         {
    #             "bass_dt": "20260128",
    #             "wday_dvsn_cd": "04",
    #             "bzdy_yn": "Y",
    #             "tr_day_yn": "Y",
    #             "opnd_yn": "Y",
    #             "sttl_day_yn": "Y"
    #         }
    #     ],
    #     "rt_cd": "0",
    #     "msg_cd": "KIOK0500",
    #     "msg1": "조회가 계속됩니다..다음버튼을 Click 하십시오.                                   "
    # }
    # 
    bass_dt = "20260105"
    trading_day_details = await client.rest_client.get_quotations_chk_holiday_v1_async(bass_dt=bass_dt)

    print(f"========== test_get_quotations_chk_holiday_v1_async ==========")
    for trading_day_detail in trading_day_details["output"]:
        if trading_day_detail["bass_dt"] == bass_dt and trading_day_detail["opnd_yn"] == "Y":
            assert True



