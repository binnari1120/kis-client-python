import pathlib
from datetime import datetime, timezone, timedelta
from typing import Any

import pytest
import yaml

from kis_client.domestic_spot.enums.kis_domestic_spot_afhr_flpr_yn import \
    KoreaInvestmentSecuritiesDomesticSpotAfhrFlprYn
from kis_client.domestic_spot.enums.kis_domestic_spot_excg_id_dvsn_cd import \
    KoreaInvestmentSecuritiesDomesticSpotExcgIdDvsnCd
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
                                                                       private_key=accounts["Spot"]["private_key"],
                                                                       is_corporate_account=True)
        client.set_credentials(credentials=credentials)
        token_details = await client.public_rest_client.get_token_async()
        # print(token_details)
        access_token = token_details["access_token"]
        access_token_expiration = token_details["access_token_token_expired"]

        account["access_token"] = access_token
        account["access_token_expiration"] = access_token_expiration

        _save(accounts)


@pytest.mark.asyncio
async def test_post_cash_v1_async():
    # return
    _set_access_token()

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"],
                                                                   is_corporate_account=False)
    client.set_credentials(credentials=credentials)

    cano = "81382087"
    acnt_prdt_cd = "01"
    pdno = "088350"  # 한화생명
    ord_qty = "1"
    excg_id_dvsn_cd = KoreaInvestmentSecuritiesDomesticSpotExcgIdDvsnCd.SOR

    # 시장가 매수
    # is_closing = False
    # sll_type = None
    # ord_dvsn = "01" # 시장가
    # ord_unpr = "0"

    # # 지정가 매수
    is_closing = False
    sll_type = None
    ord_dvsn = "00" # 지정가
    ord_unpr = "2900"

    # # 지정가 매도
    # is_closing = True
    # sll_type = None
    # ord_dvsn = "00" # 지정가
    # ord_unpr = "3150"
    #
    # # 시장가가 매도
    # is_closing = True
    # sll_type = None
    # ord_dvsn = "01" # 시장가
    # ord_unpr = "0"

    result = await client.private_rest_client.post_trading_order_cash_v1_async(cano=cano,
                                                                               acnt_prdt_cd=acnt_prdt_cd,
                                                                               pdno=pdno,
                                                                               ord_dvsn=ord_dvsn,
                                                                               ord_qty=ord_qty,
                                                                               is_closing=is_closing,
                                                                               sll_type=sll_type,
                                                                               ord_unpr=ord_unpr,
                                                                               excg_id_dvsn_cd=excg_id_dvsn_cd)

    # {
    #     "rt_cd": "0",
    #     "msg_cd": "APBK0013",
    #     "msg1": "주문 전송 완료 되었습니다.",
    #     "output": {
    #         "KRX_FWDG_ORD_ORGNO": "03930",
    #         "ODNO": "0000085100",
    #         "ORD_TMD": "094414",
    #         "SOR_ODNO": ""
    #     }
    # }

    print(result)
    match result["msg_cd"]:
        case "APBK0918":
            assert result["msg1"] == "장운영시간이 아닙니다.(주문불가)"
        case "APBK0919":
            assert result["msg1"] == "장운영일자가 주문일과 상이합니다"
        case "APBK0013":
            assert result["msg1"] == "주문 전송 완료 되었습니다."

@pytest.mark.asyncio
async def test_get_psbl_rvsecncl_v1_async():
    _set_access_token()

    cano = "81382087"
    acnt_prdt_cd = "01"
    afhr_flp_yn = KoreaInvestmentSecuritiesDomesticSpotAfhrFlprYn.N
    inqr_dvsn = "02"
    fund_sttl_icld_yn = "Y"
    prcs_dvsn = "01"

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"],
                                                                   is_corporate_account=False)
    client.set_credentials(credentials=credentials)

    order_details = await client.private_rest_client.get_trading_inquire_psbl_rvsecncl_v1_async(cano=cano,
                                                                                                acnt_prdt_cd=acnt_prdt_cd,
                                                                                                inqr_dvsn_1="0",
                                                                                                inqr_dvsn_2="1")
    print(order_details)

    # [
    #     {
    #         "pdno": "088350",
    #         "prdt_name": "한화생명",
    #         "trad_dvsn_name": "현금",
    #         "bfdy_buy_qty": "0",
    #         "bfdy_sll_qty": "0",
    #         "thdt_buyqty": "1",
    #         "thdt_sll_qty": "0",
    #         "hldg_qty": "1",
    #         "ord_psbl_qty": "1",
    #         "pchs_avg_pric": "3145.0000",
    #         "pchs_amt": "3145",
    #         "prpr": "3145",
    #         "evlu_amt": "3145",
    #         "evlu_pfls_amt": "0",
    #         "evlu_pfls_rt": "0.00",
    #         "evlu_erng_rt": "0.00000000",
    #         "loan_dt": "",
    #         "loan_amt": "0",
    #         "stln_slng_chgs": "0",
    #         "expd_dt": "",
    #         "fltt_rt": "1.94489465",
    #         "bfdy_cprs_icdc": "60",
    #         "item_mgna_rt_name": "30%",
    #         "grta_rt_name": "45%",
    #         "sbst_pric": "2340",
    #         "stck_loan_unpr": "0.0000"
    #     }
    # ]
    print(order_details)
    print(order_details["output"])
    print(order_details["ctx_area_fk100"])
    print("==========")

@pytest.mark.asyncio
async def test_get_balance_v1_async():
    _set_access_token()

    cano = "81382087"
    acnt_prdt_cd = "01"
    afhr_flp_yn = KoreaInvestmentSecuritiesDomesticSpotAfhrFlprYn.N
    inqr_dvsn = "02"
    fund_sttl_icld_yn = "Y"
    prcs_dvsn = "01"

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"],
                                                                   is_corporate_account=False)
    client.set_credentials(credentials=credentials)

    balance_details = await client.private_rest_client.get_trading_inquire_balance_v1_async(cano=cano,
                                                                                            acnt_prdt_cd=acnt_prdt_cd,
                                                                                            afhr_flp_yn=afhr_flp_yn,
                                                                                            inqr_dvsn=inqr_dvsn,
                                                                                            fund_sttl_icld_yn=fund_sttl_icld_yn,
                                                                                            prcs_dvsn=prcs_dvsn)
    print(balance_details)

    # [
    #     {
    #         "pdno": "088350",
    #         "prdt_name": "한화생명",
    #         "trad_dvsn_name": "현금",
    #         "bfdy_buy_qty": "0",
    #         "bfdy_sll_qty": "0",
    #         "thdt_buyqty": "1",
    #         "thdt_sll_qty": "0",
    #         "hldg_qty": "1",
    #         "ord_psbl_qty": "1",
    #         "pchs_avg_pric": "3145.0000",
    #         "pchs_amt": "3145",
    #         "prpr": "3145",
    #         "evlu_amt": "3145",
    #         "evlu_pfls_amt": "0",
    #         "evlu_pfls_rt": "0.00",
    #         "evlu_erng_rt": "0.00000000",
    #         "loan_dt": "",
    #         "loan_amt": "0",
    #         "stln_slng_chgs": "0",
    #         "expd_dt": "",
    #         "fltt_rt": "1.94489465",
    #         "bfdy_cprs_icdc": "60",
    #         "item_mgna_rt_name": "30%",
    #         "grta_rt_name": "45%",
    #         "sbst_pric": "2340",
    #         "stck_loan_unpr": "0.0000"
    #     }
    # ]


@pytest.mark.asyncio
async def test_get_balance_v1_async():
    _set_access_token()

    cano = "81382087"
    acnt_prdt_cd = "01"
    afhr_flp_yn = KoreaInvestmentSecuritiesDomesticSpotAfhrFlprYn.N
    inqr_dvsn = "02"
    fund_sttl_icld_yn = "Y"
    prcs_dvsn = "01"

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"],
                                                                   is_corporate_account=False)
    client.set_credentials(credentials=credentials)

    balance_details = await client.private_rest_client.get_trading_inquire_balance_v1_async(cano=cano,
                                                                                            acnt_prdt_cd=acnt_prdt_cd,
                                                                                            afhr_flp_yn=afhr_flp_yn,
                                                                                            inqr_dvsn=inqr_dvsn,
                                                                                            fund_sttl_icld_yn=fund_sttl_icld_yn,
                                                                                            prcs_dvsn=prcs_dvsn)
    print(balance_details)
    print(balance_details["ctx_area_fk100"])
    print(balance_details["output1"])
    print(balance_details["output2"])
    print("==========")


@pytest.mark.asyncio
async def test_get_balance_rlz_pl_v1_async():
    _set_access_token()

    cano = "81382087"
    acnt_prdt_cd = "01"
    afhr_flp_yn = KoreaInvestmentSecuritiesDomesticSpotAfhrFlprYn.N
    inqr_dvsn = "02"
    fund_sttl_icld_yn = "Y"
    prcs_dvsn = "01"

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"],
                                                                   is_corporate_account=False)
    client.set_credentials(credentials=credentials)

    balance_details = await client.private_rest_client.get_trading_inquire_balance_rlz_pl_v1_async(cano=cano,
                                                                                                   acnt_prdt_cd=acnt_prdt_cd,
                                                                                                   afhr_flp_yn=afhr_flp_yn,
                                                                                                   inqr_dvsn=inqr_dvsn,
                                                                                                   fund_sttl_icld_yn=fund_sttl_icld_yn,
                                                                                                   prcs_dvsn=prcs_dvsn,
                                                                                                   ctx_area_fk100="81382087^01^N^N^02^01^Y^")
    print(balance_details)
    print(balance_details["ctx_area_fk100"])
    print(balance_details["output1"])
    print(balance_details["output2"])
    print("==========")


# @pytest.mark.asyncio
# async def test_get_psbl_sell_v1_async():
#     _set_access_token()
#
#     cano = "81382087"
#     acnt_prdt_cd = "01"
#     afhr_flp_yn = KoreaInvestmentSecuritiesDomesticSpotAfhrFlprYn.N
#     inqr_dvsn = "02"
#     fund_sttl_icld_yn = "Y"
#     prcs_dvsn = "01"
#
#     with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
#         accounts = yaml.safe_load(file)
#     credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
#                                                                    private_key=accounts["Spot"]["private_key"],
#                                                                    is_corporate_account=False)
#     client.set_credentials(credentials=credentials)
#
#     balance_details = await client.private_rest_client.get_psbl_sell_v1_async(cano=cano,
#                                                                               acnt_prdt_cd=acnt_prdt_cd,
#                                                                               afhr_flp_yn=afhr_flp_yn,
#                                                                               inqr_dvsn=inqr_dvsn,
#                                                                               fund_sttl_icld_yn=fund_sttl_icld_yn,
#                                                                               prcs_dvsn=prcs_dvsn)
#     print(balance_details)


@pytest.mark.asyncio
async def test_get_account_balance_v1_async():
    _set_access_token()

    cano = "81382087"
    acnt_prdt_cd = "21"

    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
        accounts = yaml.safe_load(file)
    credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
                                                                   private_key=accounts["Spot"]["private_key"],
                                                                   is_corporate_account=False)
    client.set_credentials(credentials=credentials)

    balance_details = await client.private_rest_client.get_trading_inquire_account_balance_v1_async(cano=cano,
                                                                                                    acnt_prdt_cd=acnt_prdt_cd)
    print(balance_details)
