import pathlib

import pytest
import yaml

from kis_client.domestic_stock.enums.kis_domestic_stock_ccld_dvsn import KoreaInvestmentSecuritiesDomesticStockCcldDvsn
from kis_client.domestic_stock.enums.kis_domestic_stock_afhr_flpr_yn import \
    KoreaInvestmentSecuritiesDomesticStockAfhrFlprYn
from kis_client.domestic_stock.enums.kis_domestic_stock_excg_id_dvsn_cd import \
    KoreaInvestmentSecuritiesDomesticStockExcgIdDvsnCd
from kis_client.domestic_stock.enums.kis_domestic_stock_sll_buy_dvsn_cd import \
    KoreaInvestmentSecuritiesDomesticStockSllBuyDvsnCd
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
async def test_post_cash_v1_async():
    return
    cano = "81382087"
    acnt_prdt_cd = "01"
    pdno = "088350"  # 한화생명
    pdno = "010140"
    ord_qty = "1"
    excg_id_dvsn_cd = KoreaInvestmentSecuritiesDomesticStockExcgIdDvsnCd.SOR

    # 시장가 매수
    # is_closing = False
    # sll_type = None
    # ord_dvsn = "01" # 시장가
    # ord_unpr = "0"

    # # 지정가 매수
    is_closing = False
    sll_type = None
    ord_dvsn = "00"  # 지정가
    ord_unpr = "2900"
    ord_unpr = "23150"

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

    result = await client.rest_client._post_trading_order_cash_v1_async(cano=cano,
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
async def test_post_trading_order_rvsecncl_v1_async():
    cano = "81382087"
    acnt_prdt_cd = "01"
    krx_fwdg_ord_ordno = ""
    orgn_odno = "0000574900"
    ord_dvsn = "00"
    rvse_cncl_dvsn_cd = "02"
    ord_qty = "1"
    ord_unpr = "0"
    qty_all_ord_yn = "Y"
    excg_id_dvsn_cd = KoreaInvestmentSecuritiesDomesticStockExcgIdDvsnCd.SOR

    result = await client.rest_client.post_trading_order_rvsecncl_v1_async(cano=cano,
                                                                           acnt_prdt_cd=acnt_prdt_cd,
                                                                           krx_fwdg_ord_ordno=krx_fwdg_ord_ordno,
                                                                           orgn_odno=orgn_odno,
                                                                           ord_dvsn=ord_dvsn,
                                                                           rvse_cncl_dvsn_cd=rvse_cncl_dvsn_cd,
                                                                           ord_qty=ord_qty,
                                                                           ord_unpr=ord_unpr,
                                                                           qty_all_ord_yn=qty_all_ord_yn,
                                                                           excg_id_dvsn_cd=excg_id_dvsn_cd)

    # {
    #     "rt_cd": "0",
    #     "msg_cd": "APBK0013",
    #     "msg1": "주문 전송 완료 되었습니다.",
    #     "output": {
    #         "KRX_FWDG_ORD_ORGNO": "03930",
    #         "ODNO": "0000503800",
    #         "ORD_TMD": "152400",
    #         "SOR_ODNO": ""
    #     }
    # }

    print(f"========== test_post_trading_order_rvsecncl_v1_async ==========")
    print(result)
    match result["msg_cd"]:
        case "APBK0918":
            assert result["msg1"] == "장운영시간이 아닙니다.(주문불가)"
        case "APBK0919":
            assert result["msg1"] == "장운영일자가 주문일과 상이합니다"
        case "APBK0013":
            assert result["msg1"] == "주문 전송 완료 되었습니다."
        case "APBK0963":  # rt_cd: 7
            assert result["msg1"] == "주문구분코드 오류 입니다."
        case "APBK0927":  # rt_cd: 7
            assert result["msg1"] == "정정취소 가능수량이 없습니다."


@pytest.mark.asyncio
async def test_get_trading_inquire_daily_ccld_v1_async():
    # {
    #     "ctx_area_fk100": "81382087!^01!^20251201!^20260104!^00000A088350!^01!^00!^00!^                                        ",
    #     "ctx_area_nk100": "                                                                                                    ",
    #     "output1": [
    #         {
    #             "ord_dt": "20251217",
    #             "ord_gno_brno": "03930",
    #             "odno": "0000085100",
    #             "orgn_odno": "",
    #             "ord_dvsn_name": "시장가",
    #             "sll_buy_dvsn_cd": "02",
    #             "sll_buy_dvsn_cd_name": "현금매수",
    #             "pdno": "088350",
    #             "prdt_name": "한화생명",
    #             "ord_qty": "1",
    #             "ord_unpr": "0",
    #             "ord_tmd": "094414",
    #             "tot_ccld_qty": "1",
    #             "avg_prvs": "3145",
    #             "cncl_yn": "",
    #             "tot_ccld_amt": "3145",
    #             "loan_dt": "",
    #             "ordr_empno": "OpnAPI",
    #             "ord_dvsn_cd": "01",
    #             "cncl_cfrm_qty": "0",
    #             "rmn_qty": "0",
    #             "rjct_qty": "0",
    #             "ccld_cndt_name": "없음",
    #             "inqr_ip_addr": "211.206.164.254",
    #             "cpbc_ordp_ord_rcit_dvsn_cd": "",
    #             "cpbc_ordp_infm_mthd_dvsn_cd": "",
    #             "infm_tmd": "",
    #             "ctac_tlno": "",
    #             "prdt_type_cd": "",
    #             "excg_dvsn_cd": "12",
    #             "cpbc_ordp_mtrl_dvsn_cd": "",
    #             "ord_orgno": "00000",
    #             "rsvn_ord_end_dt": "",
    #             "excg_id_dvsn_cd": "SOR",
    #             "stpm_cndt_pric": "0",
    #             "stpm_efct_occr_dtmd": ""
    #         }
    #     ],
    #     "output2": {
    #         "tot_ord_qty": "1",
    #         "tot_ccld_qty": "1",
    #         "tot_ccld_amt": "3145",
    #         "prsm_tlex_smtl": "0",
    #         "pchs_avg_pric": "3145.0000"
    #     },
    #     "rt_cd": "0",
    #     "msg_cd": "KIOK0460",
    #     "msg1": "조회 되었습니다. (마지막 자료)                                                  "
    # }
    cano = "81382087"
    acnt_prdt_cd = "01"
    inqr_strt_dt = "20251201"
    inqr_end_dt = "20260104"
    sll_buy_dvsn_cd = KoreaInvestmentSecuritiesDomesticStockSllBuyDvsnCd.Buy
    pdno = "088350"  # 한화생명
    ord_gno_brno = ""
    ccld_dvsn = KoreaInvestmentSecuritiesDomesticStockCcldDvsn.Filled
    inqr_dvsn = "00"
    inqr_dvsn_3 = "00"
    excg_id_dvsn_cd = KoreaInvestmentSecuritiesDomesticStockExcgIdDvsnCd.SOR

    result = await client.rest_client.get_trading_inquire_daily_ccld_v1_async(cano=cano,
                                                                              acnt_prdt_cd=acnt_prdt_cd,
                                                                              inqr_strt_dt=inqr_strt_dt,
                                                                              inqr_end_dt=inqr_end_dt,
                                                                              sll_buy_dvsn_cd=sll_buy_dvsn_cd,
                                                                              pdno=pdno,
                                                                              ord_gno_brno=ord_gno_brno,
                                                                              ccld_dvsn=ccld_dvsn,
                                                                              inqr_dvsn=inqr_dvsn,
                                                                              inqr_dvsn_3=inqr_dvsn_3,
                                                                              excg_id_dvsn_cd=excg_id_dvsn_cd)


    print(f"========== test_get_trading_inquire_daily_ccld_v1_async ==========")
    print(result)


# @pytest.mark.asyncio
# async def test_post_trading_inquire_psbl_rvsecncl_v1_async():
#     _set_access_token()
#
#     cano = "81382087"
#     acnt_prdt_cd = "01"
#     pdno = "088350"  # 한화생명
#     ord_qty = "1"
#     sll_buy_dnsn_cd = KoreaInvestmentSecuritiesDomesticSpotSllBuyDvsnCd.Buy
#     ord_dvsn_cd = ""
#     ord_objt_cblc_dvsn_cd = ""
#     rsvn_ord_seq = "0000549400"
#
#     with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml") as file:
#         accounts = yaml.safe_load(file)
#     credentials = KoreaInvestmentSecuritiesDomesticSpotCredentials(public_key=accounts["Spot"]["public_key"],
#                                                                    private_key=accounts["Spot"]["private_key"],
#                                                                    is_corporate_account=False)
#     client.set_credentials(credentials=credentials)
#     result = await client.private_rest_client.post_trading_inquire_psbl_rvsecncl_v1_async(cano=cano,
#                                                                                           acnt_prdt_cd=acnt_prdt_cd,
#                                                                                           pdno=pdno,
#                                                                                           ord_qty=ord_qty,
#                                                                                           sll_buy_dnsn_cd=sll_buy_dnsn_cd,
#                                                                                           ord_dvsn_cd=ord_dvsn_cd,
#                                                                                           ord_objt_cblc_dvsn_cd=ord_objt_cblc_dvsn_cd,
#                                                                                           rsvn_ord_seq=rsvn_ord_seq,
#                                                                                           is_cancelling=True)
#     print(result)


@pytest.mark.asyncio
async def test_get_trading_inquire_psbl_rvsecncl_v1_async():
    cano = "81382087"
    acnt_prdt_cd = "01"
    afhr_flp_yn = KoreaInvestmentSecuritiesDomesticStockAfhrFlprYn.N
    inqr_dvsn = "02"
    fund_sttl_icld_yn = "Y"
    prcs_dvsn = "01"

    order_details = await client.rest_client.get_trading_inquire_psbl_rvsecncl_v1_async(cano=cano,
                                                                                        acnt_prdt_cd=acnt_prdt_cd,
                                                                                        inqr_dvsn_1="0",
                                                                                        inqr_dvsn_2="0")
    assert "output" in order_details
    for order_detail in order_details["output"]:
        assert "ord_gno_brno" in order_detail
        assert "odno" in order_detail
        assert "orgn_odno" in order_detail
        assert "ord_dvsn_name" in order_detail
        assert "pdno" in order_detail
        assert "prdt_name" in order_detail
        assert "rvse_cncl_dvsn_name" in order_detail
        assert "ord_qty" in order_detail
        assert "ord_unpr" in order_detail
        assert "ord_tmd" in order_detail
        assert "tot_ccld_qty" in order_detail
        assert "tot_ccld_amt" in order_detail
        assert "psbl_qty" in order_detail
        assert "sll_buy_dvsn_cd" in order_detail
        assert "ord_dvsn_cd" in order_detail
        assert "mgco_aptm_odno" in order_detail
        assert "excg_dvsn_cd" in order_detail
        assert "excg_id_dvsn_cd" in order_detail
        assert "excg_id_dvsn_name" in order_detail
        assert "stpm_cndt_pric" in order_detail
        assert "stpm_efct_occr_yn" in order_detail

    # {
    #     "ctx_area_fk100": "81382087^01^                                                                                        ",
    #     "ctx_area_nk100": "                                                                                                    ",
    #     "output": [
    #         {
    #             "ord_gno_brno": "03930",
    #             "odno": "0000457500",
    #             "orgn_odno": "",
    #             "ord_dvsn_name": "지정가",
    #             "pdno": "088350",
    #             "prdt_name": "한화생명",
    #             "rvse_cncl_dvsn_name": "현금매수",
    #             "ord_qty": "1",
    #             "ord_unpr": "2900",
    #             "ord_tmd": "152229",
    #             "tot_ccld_qty": "0",
    #             "tot_ccld_amt": "0",
    #             "psbl_qty": "1",
    #             "sll_buy_dvsn_cd": "02",
    #             "ord_dvsn_cd": "00",
    #             "mgco_aptm_odno": "",
    #             "excg_dvsn_cd": "12",
    #             "excg_id_dvsn_cd": "SOR",
    #             "excg_id_dvsn_name": "SOR",
    #             "stpm_cndt_pric": "0",
    #             "stpm_efct_occr_yn": ""
    #         },
    #         {
    #             "ord_gno_brno": "03930",
    #             "odno": "0000456600",
    #             "orgn_odno": "",
    #             "ord_dvsn_name": "지정가",
    #             "pdno": "088350",
    #             "prdt_name": "한화생명",
    #             "rvse_cncl_dvsn_name": "현금매수",
    #             "ord_qty": "1",
    #             "ord_unpr": "2900",
    #             "ord_tmd": "151849",
    #             "tot_ccld_qty": "0",
    #             "tot_ccld_amt": "0",
    #             "psbl_qty": "1",
    #             "sll_buy_dvsn_cd": "02",
    #             "ord_dvsn_cd": "00",
    #             "mgco_aptm_odno": "",
    #             "excg_dvsn_cd": "12",
    #             "excg_id_dvsn_cd": "SOR",
    #             "excg_id_dvsn_name": "SOR",
    #             "stpm_cndt_pric": "0",
    #             "stpm_efct_occr_yn": ""
    #         }
    #     ],
    #     "rt_cd": "0",
    #     "msg_cd": "KIOK0510",
    #     "msg1": "조회가 완료되었습니다                                                           "
    # }

    print(f"========== test_get_trading_inquire_psbl_rvsecncl_v1_async ==========")
    print(order_details)
    # print(order_details["output"])
    # print(order_details["ctx_area_fk100"])
    print("==========")


@pytest.mark.asyncio
async def test_get_trading_inquire_balance_v1_async():
    cano = "81382087"
    acnt_prdt_cd = "01"
    afhr_flp_yn = KoreaInvestmentSecuritiesDomesticStockAfhrFlprYn.N
    inqr_dvsn = "02"
    fund_sttl_icld_yn = "Y"
    prcs_dvsn = "01"

    balance_details = await client.rest_client.get_trading_inquire_balance_v1_async(cano=cano,
                                                                                    acnt_prdt_cd=acnt_prdt_cd,
                                                                                    afhr_flp_yn=afhr_flp_yn,
                                                                                    inqr_dvsn=inqr_dvsn,
                                                                                    fund_sttl_icld_yn=fund_sttl_icld_yn,
                                                                                    prcs_dvsn=prcs_dvsn)
    print(f"========== test_get_trading_inquire_balance_v1_async ==========")
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
async def test_get_trading_inquire_balance_v1_async():
    cano = "81382087"
    acnt_prdt_cd = "01"
    afhr_flp_yn = KoreaInvestmentSecuritiesDomesticStockAfhrFlprYn.N
    inqr_dvsn = "02"
    fund_sttl_icld_yn = "Y"
    prcs_dvsn = "01"

    balance_details = await client.rest_client.get_trading_inquire_balance_v1_async(cano=cano,
                                                                                    acnt_prdt_cd=acnt_prdt_cd,
                                                                                    afhr_flp_yn=afhr_flp_yn,
                                                                                    inqr_dvsn=inqr_dvsn,
                                                                                    fund_sttl_icld_yn=fund_sttl_icld_yn,
                                                                                    prcs_dvsn=prcs_dvsn)
    print(f"========== test_get_trading_inquire_balance_v1_async ==========")
    print(balance_details)
    # print(balance_details["ctx_area_fk100"])
    # print(balance_details["output1"])
    # print(balance_details["output2"])
    print("==========")


# @pytest.mark.asyncio
# async def test_get_trading_inquire_balance_rlz_pl_v1_async():
#     cano = "81382087"
#     acnt_prdt_cd = "01"
#     afhr_flp_yn = KoreaInvestmentSecuritiesDomesticStockAfhrFlprYn.N
#     inqr_dvsn = "02"
#     fund_sttl_icld_yn = "Y"
#     prcs_dvsn = "01"
#
#     balance_details = await client.rest_client.get_trading_inquire_balance_rlz_pl_v1_async(cano=cano,
#                                                                                            acnt_prdt_cd=acnt_prdt_cd,
#                                                                                            afhr_flp_yn=afhr_flp_yn,
#                                                                                            inqr_dvsn=inqr_dvsn,
#                                                                                            fund_sttl_icld_yn=fund_sttl_icld_yn,
#                                                                                            prcs_dvsn=prcs_dvsn)
#     print(f"========== test_get_trading_inquire_balance_rlz_pl_v1_async ==========")
#     print(balance_details)


@pytest.mark.asyncio
async def test_get_trading_inquire_account_balance_v1_async():
    cano = "81382087"
    acnt_prdt_cd = "21"

    balance_details = await client.rest_client.get_trading_inquire_account_balance_v1_async(cano=cano,
                                                                                            acnt_prdt_cd=acnt_prdt_cd)
    print(f"========== test_get_trading_inquire_account_balance_v1_async ==========")
    print(balance_details)


# 투자계좌자산현황조회
@pytest.mark.asyncio
async def test_get_trading_inquire_psbl_order_v1_async():
    cano = "81382087"
    acnt_prdt_cd = "01"
    pdno = "088350"  # 한화생명
    ord_unpr = ""
    ord_dvsn = "01"
    cma_evlu_amt_icld_yn = "Y"
    ovrs_icld_yn = "Y"

    balance_details = await client.rest_client.get_trading_inquire_psbl_order_v1_async(cano=cano,
                                                                                       acnt_prdt_cd=acnt_prdt_cd,
                                                                                       pdno=pdno,
                                                                                       ord_unpr=ord_unpr,
                                                                                       ord_dvsn=ord_dvsn,
                                                                                       cma_evlu_amt_icld_yn=cma_evlu_amt_icld_yn,
                                                                                       ovrs_icld_yn=ovrs_icld_yn)
    print(f"========== test_get_trading_inquire_psbl_order_v1_async ==========")
    print(balance_details)


@pytest.mark.asyncio
async def test_get_trading_inquire_psbl_sell_v1_async():
    cano = "81382087"
    acnt_prdt_cd = "01"
    pdno = "088350"  # 한화생명

    position_details = await client.rest_client.get_trading_inquire_psbl_sell_v1_async(cano=cano,
                                                                                       acnt_prdt_cd=acnt_prdt_cd,
                                                                                       pdno=pdno)
    print(f"========== test_get_trading_inquire_psbl_sell_v1_async ==========")
    print(position_details)
