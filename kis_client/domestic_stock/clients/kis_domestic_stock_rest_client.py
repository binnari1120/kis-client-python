from typing import Dict
from typing import Optional, Any, Union

from kis_client.domestic_stock.enums.kis_domestic_stock_ccld_dvsn import KoreaInvestmentSecuritiesDomesticStockCcldDvsn
from kis_client.domestic_stock.enums.kis_domestic_stock_fid_input_iscd import KoreaInvestmentSecuritiesDomesticStockFidInputIscd
from kis_client.domestic_stock.constants.kis_domestic_stock_endpoints import *
from kis_client.domestic_stock.core.kis_domestic_stock_api_call_executor import \
    KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor
from kis_client.domestic_stock.enums.kis_domestic_stock_afhr_flpr_yn import \
    KoreaInvestmentSecuritiesDomesticStockAfhrFlprYn
from kis_client.domestic_stock.enums.kis_domestic_stock_excg_id_dvsn_cd import \
    KoreaInvestmentSecuritiesDomesticStockExcgIdDvsnCd
from kis_client.domestic_stock.enums.kis_domestic_stock_fid_cond_mrkt_div_code import \
    KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode
from kis_client.domestic_stock.enums.kis_domestic_stock_fid_div_cls_code import \
    KoreaInvestmentSecuritiesDomesticStockFidDivClsCode
from kis_client.domestic_stock.enums.kis_domestic_stock_fid_period_div_cd import \
    KoreaInvestmentSecuritiesDomesticStockFidPeriodDivCd
from kis_client.domestic_stock.enums.kis_domestic_stock_sll_buy_dvsn_cd import \
    KoreaInvestmentSecuritiesDomesticStockSllBuyDvsnCd
from kis_client.domestic_stock.models.kis_domestic_stock_credentials import \
    KoreaInvestmentSecuritiesDomesticStockCredentials


class KoreaInvestmentSecuritiesDomesticStockRestClient:
    RECV_WINDOW = 50000

    def __init__(self, executor: KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor):
        self._credential: Optional[KoreaInvestmentSecuritiesDomesticStockCredentials] = None
        self._executor = executor
        self._access_token: Optional[str] = None
        self._headers: Optional[Dict] = None

    def set_credentials(self,
                        credentials: KoreaInvestmentSecuritiesDomesticStockCredentials):
        self._credential = credentials

    def set_access_token(self,
                         access_token: str):
        self._access_token = access_token
        self._headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

    def _ensure_credentials(self):
        if self._credential is None:
            raise ValueError("Please set credentials!")

    def _ensure_access_token(self):
        if self._access_token is None:
            raise ValueError("Please set access token!")

    '''
        분류: [국내주식] 주문/계좌
        역할: 주식주문(현금)
    '''
    async def post_trading_order_cash_v1_async(self,
                                               cano: str,
                                               acnt_prdt_cd: str,
                                               pdno: str,
                                               ord_dvsn: str,
                                               ord_qty: str,
                                               is_closing: bool = False,
                                               sll_type: Optional[str] = None,
                                               ord_unpr: str = "0",
                                               cndt_pric: Optional[str] = None,
                                               excg_id_dvsn_cd: Optional[
                                                   KoreaInvestmentSecuritiesDomesticStockExcgIdDvsnCd] = None):
        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
            "ORD_DVSN": ord_dvsn,
            "ORD_QTY": ord_qty,
            "ORD_UNPR": ord_unpr
        })

        if sll_type is not None:
            parameters["SLL_TYPE"] = sll_type
        if cndt_pric is not None:
            parameters["CNDT_PRIC"] = cndt_pric
        if excg_id_dvsn_cd is not None:
            parameters["EXCG_ID_DVSN_CD"] = excg_id_dvsn_cd.value

        if is_closing:
            if self._credential.is_demo_account:
                tr_id = "VTTC0011U"
            else:
                tr_id = "TTTC0011U"
        else:
            if self._credential.is_demo_account:
                tr_id = "VTTC0012U"
            else:
                tr_id = "TTTC0012U"

        self._headers["tr_id"] = tr_id

        try:
            data = await self._executor.execute_private_api_call_async(http_method="post",
                                                                       endpoint=TRADING_ORDER_CASH_V1,
                                                                       headers=self._headers,
                                                                       parameters=parameters)
            return data
        except Exception:
            raise

    '''
        분류: [국내주식] 주문/계좌
        역할: 주식주문(정정취소)
    '''
    async def post_trading_order_rvsecncl_v1_async(self,
                                                   cano: str,
                                                   acnt_prdt_cd: str,
                                                   krx_fwdg_ord_ordno: str,
                                                   orgn_odno: str,
                                                   ord_dvsn: str,
                                                   rvse_cncl_dvsn_cd: str,
                                                   ord_qty: str,
                                                   ord_unpr: str,
                                                   qty_all_ord_yn: str,
                                                   cndt_pric: Optional[str] = None,
                                                   excg_id_dvsn_cd: Optional[
                                                       KoreaInvestmentSecuritiesDomesticStockExcgIdDvsnCd] = None):
        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "KRX_FWDG_ORD_ORGNO": krx_fwdg_ord_ordno,
            "ORD_QTY": ord_qty
        })

        if ord_unpr is not None:
            parameters["ORD_UNPR"] = ord_unpr
        if acnt_prdt_cd is not None:
            parameters["ACNT_PRDT_CD"] = acnt_prdt_cd
        if krx_fwdg_ord_ordno is not None:
            parameters["KRX_FWDG_ORD_ORGNO"] = krx_fwdg_ord_ordno
        if orgn_odno is not None:
            parameters["ORGN_ODNO"] = orgn_odno
        if ord_dvsn is not None:
            parameters["ORD_DVSN"] = ord_dvsn
        if rvse_cncl_dvsn_cd is not None:
            parameters["RVSE_CNCL_DVSN_CD"] = rvse_cncl_dvsn_cd
        if ord_qty is not None:
            parameters["ORD_QTY"] = ord_qty
        if ord_unpr is not None:
            parameters["ORD_UNPR"] = ord_unpr
        if qty_all_ord_yn is not None:
            parameters["QTY_ALL_ORD_YN"] = qty_all_ord_yn
        if cndt_pric is not None:
            parameters["CNDT_PRIC"] = cndt_pric
        if excg_id_dvsn_cd is not None:
            parameters["EXCG_ID_DVSN_CD"] = excg_id_dvsn_cd.value

        self._headers["tr_id"] = "VTTC0013U" if self._credential.is_demo_account else "TTTC0013U"

        try:
            data = await self._executor.execute_private_api_call_async(http_method="post",
                                                                       endpoint=TRADING_ORDER_RVSECNCL_V1,
                                                                       headers=self._headers,
                                                                       parameters=parameters)
            return data
        except Exception:
            raise

    '''
        분류: [국내주식] 주문/계좌
        역할: 주식일별주문체결조회
    '''
    async def get_trading_inquire_daily_ccld_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str,
            inqr_strt_dt: str,
            inqr_end_dt: str,
            sll_buy_dvsn_cd: KoreaInvestmentSecuritiesDomesticStockSllBuyDvsnCd,
            pdno: str,
            ord_gno_brno: str,
            ccld_dvsn: KoreaInvestmentSecuritiesDomesticStockCcldDvsn,
            inqr_dvsn: str,
            inqr_dvsn_3: str,
            excg_id_dvsn_cd: KoreaInvestmentSecuritiesDomesticStockExcgIdDvsnCd,
            odno: Optional[str] = None,
            inqr_dvsn_1: Optional[str] = None,
            ctx_area_fk100: Optional[str] = None,
            ctx_area_nk100: Optional[str] = None) -> Optional[Any]:

        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "INQR_STRT_DT": inqr_strt_dt,
            "INQR_END_DT": inqr_end_dt,
            "SLL_BUY_DVSN_CD": sll_buy_dvsn_cd.value,
            "PDNO": pdno,
            "ORD_GNO_BRNO": ord_gno_brno,
            "ODNO": "",
            "CCLD_DVSN": ccld_dvsn.value,
            "INQR_DVSN": inqr_dvsn,
            "INQR_DVSN_1": "",
            "INQR_DVSN_3": inqr_dvsn_3,
            "EXCG_ID_DVSN_CD": excg_id_dvsn_cd.value,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
        })

        if ctx_area_fk100 is not None:
            parameters["ODNO"] = odno
        if ctx_area_fk100 is not None:
            parameters["INQR_DVSN_1"] = inqr_dvsn_1
        if ctx_area_fk100 is not None:
            parameters["CTX_AREA_FK100"] = ctx_area_fk100
        if ctx_area_nk100 is not None:
            parameters["CTX_AREA_NK100"] = ctx_area_nk100

        self._headers["tr_id"] = "VTTC0081R" if self._credential.is_demo_account else "TTTC0081R"
        if 3:
            self._headers["tr_id"] = "VTSC9215R" if self._credential.is_demo_account else "CTSC9215R"

        try:
            data = await self._executor.execute_private_api_call_async(http_method="get",
                                                                       endpoint=TRADING_ORDER_RESV_CCNL_V1,
                                                                       headers=self._headers,
                                                                       parameters=parameters)
            return data
        except Exception:
            raise

    '''
        분류: [국내주식] 주문/계좌
        역할: 주식정정취소가능주문조회
    '''
    async def get_trading_inquire_balance_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str,
            afhr_flp_yn: KoreaInvestmentSecuritiesDomesticStockAfhrFlprYn,
            inqr_dvsn: str,  # 01 or 02
            fund_sttl_icld_yn: str,  # N or Y
            prcs_dvsn: str,  # 00 or 01
            ctx_area_fk100: Optional[str] = None,
            ctx_area_nk100: Optional[str] = None) -> Optional[Any]:

        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "AFHR_FLPR_YN": afhr_flp_yn.value,
            "OFL_YN": "",
            "INQR_DVSN": inqr_dvsn,
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": fund_sttl_icld_yn,
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": prcs_dvsn,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
        })

        if ctx_area_fk100 is not None:
            parameters["CTX_AREA_FK100"] = ctx_area_fk100
        if ctx_area_nk100 is not None:
            parameters["CTX_AREA_NK100"] = ctx_area_nk100

        self._headers["tr_id"] = "VTTC8434R" if self._credential.is_demo_account else "TTTC8434R"

        try:
            data = await self._executor.execute_private_api_call_async(http_method="get",
                                                                       endpoint=TRADING_INQUIRE_BALANCE_V1,
                                                                       headers=self._headers,
                                                                       parameters=parameters)
            return data
        except Exception:
            raise

    async def post_trading_inquire_psbl_rvsecncl_v1_async(self,
                                                          cano: str,
                                                          acnt_prdt_cd: str,
                                                          pdno: str,
                                                          ord_qty: str,
                                                          sll_buy_dnsn_cd: KoreaInvestmentSecuritiesDomesticStockSllBuyDvsnCd,
                                                          ord_dvsn_cd: str,
                                                          ord_objt_cblc_dvsn_cd: str,
                                                          rsvn_ord_seq: str,
                                                          is_cancelling: bool = True,
                                                          ord_unpr: Optional[str] = "0",
                                                          load_dt: Optional[str] = None,
                                                          rsvn_ord_end_dt: Optional[str] = None,
                                                          ctal_tlno: Optional[str] = None,
                                                          rsvn_ord_orgno: Optional[str] = None,
                                                          rsvn_ord_ord_dt: Optional[str] = None):
        self._ensure_credentials()
        if self._credential.is_demo_account:
            raise ValueError("Unsupported for demo account!")

        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
            "ORD_QTY": ord_qty
        })

        if ord_unpr is not None:
            parameters["ORD_UNPR"] = ord_unpr
        if sll_buy_dnsn_cd is not None:
            parameters["SLL_BUY_DVSN_CD"] = sll_buy_dnsn_cd.value
        if ord_dvsn_cd is not None:
            parameters["ORD_DVSN_CD"] = ord_dvsn_cd
        if ord_objt_cblc_dvsn_cd is not None:
            parameters["ORD_OBJT_CBLC_DVSN_CD"] = ord_objt_cblc_dvsn_cd
        if load_dt is not None:
            parameters["LOAN_DT"] = load_dt
        if rsvn_ord_end_dt is not None:
            parameters["RSVN_ORD_END_DT"] = rsvn_ord_end_dt
        if ctal_tlno is not None:
            parameters["CTAL_TLNO"] = ctal_tlno
        if rsvn_ord_seq is not None:
            parameters["RSVN_ORD_SEQ"] = rsvn_ord_seq
        if rsvn_ord_orgno is not None:
            parameters["RSVN_ORD_ORGNO"] = rsvn_ord_orgno
        if rsvn_ord_ord_dt is not None:
            parameters["RSVN_ORD_ORD_DT"] = rsvn_ord_ord_dt

        self._headers["tr_id"] = "CTSC0009U" if is_cancelling else "CTSC0013U"

        try:
            data = await self._executor.execute_private_api_call_async(http_method="post",
                                                                       endpoint=TRADING_ORDER_RVSECNCL_V1,
                                                                       headers=self._headers,
                                                                       parameters=parameters)
            return data
        except Exception:
            raise

    async def get_trading_inquire_psbl_rvsecncl_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str,
            inqr_dvsn_1: str,
            inqr_dvsn_2: str,
            ctx_area_fk100: Optional[str] = None,
            ctx_area_nk100: Optional[str] = None) -> Optional[Any]:

        self._ensure_credentials()
        if self._credential.is_demo_account:
            raise ValueError("Unsupported for demo account!")

        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "INQR_DVSN_1": inqr_dvsn_1,
            "INQR_DVSN_2": inqr_dvsn_2,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
        })

        if ctx_area_fk100 is not None:
            parameters["CTX_AREA_FK100"] = ctx_area_fk100
        if ctx_area_nk100 is not None:
            parameters["CTX_AREA_NK100"] = ctx_area_nk100

        self._headers["tr_id"] = "TTTC0084R"

        try:
            data = await self._executor.execute_private_api_call_async(http_method="get",
                                                                       endpoint=TRADING_INQUIRE_PSBL_RVSECNCL_V1,
                                                                       headers=self._headers,
                                                                       parameters=parameters)
            return data
        except Exception:
            raise

    async def get_trading_inquire_balance_rlz_pl_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str,
            afhr_flp_yn: KoreaInvestmentSecuritiesDomesticStockAfhrFlprYn,
            inqr_dvsn: str,  # 01 or 02
            fund_sttl_icld_yn: str,  # N or Y
            prcs_dvsn: str,  # 00 or 01
            ctx_area_fk100: Optional[str] = None,
            ctx_area_nk100: Optional[str] = None) -> Optional[Any]:

        self._ensure_credentials()
        if self._credential.is_demo_account:
            raise ValueError("Unsupported for demo account!")

        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "AFHR_FLPR_YN": afhr_flp_yn.value,
            "OFL_YN": "",
            "INQR_DVSN": inqr_dvsn,
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": fund_sttl_icld_yn,
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": prcs_dvsn,
            "COST_ICLD_YN": "1",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
        })

        if ctx_area_fk100 is not None:
            parameters["CTX_AREA_FK100"] = ctx_area_fk100
        if ctx_area_nk100 is not None:
            parameters["CTX_AREA_NK100"] = ctx_area_nk100

        self._headers["tr_id"] = "TTTC8494R"

        try:
            data = await self._executor.execute_private_api_call_async(http_method="get",
                                                                       endpoint=TRADING_INQUIRE_BALANCE_RLZ_PL_V1,
                                                                       headers=self._headers,
                                                                       parameters=parameters)
            return data
        except Exception:
            raise

    async def get_trading_order_resv_ccnl_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str,
            afhr_flp_yn: KoreaInvestmentSecuritiesDomesticStockAfhrFlprYn,
            inqr_dvsn: Union[str],  # 01 or 02
            fund_sttl_icld_yn: Union[str],  # N or Y
            prcs_dvsn: Union[str],  # 00 or 01
            ctx_area_fk100: Optional[str] = None,
            ctx_area_nk100: Optional[str] = None) -> Optional[Any]:

        self._ensure_credentials()
        if self._credential.is_demo_account:
            raise ValueError("Unsupported for demo account!")

        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "AFHR_FLPR_YN": afhr_flp_yn.value,
            "INQR_DVSN": inqr_dvsn,
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": fund_sttl_icld_yn,
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": prcs_dvsn,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
        })

        self._headers["tr_id"] = "CTSC0004R"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=TRADING_ORDER_RESV_CCNL_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_trading_inquire_account_balance_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str) -> Optional[Any]:

        self._ensure_credentials()
        if self._credential.is_demo_account:
            raise ValueError("Unsupported for demo account!")

        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "INQR_DVSN_1": "",
            "BSPR_BF_DT_APLY_YN": "",
        })

        self._headers["tr_id"] = "CTRP6548R"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=TRADING_INQUIRE_ACCOUNT_BALANCE_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_trading_inquire_psbl_order_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str,
            pdno: str,
            ord_unpr: str,
            ord_dvsn: str = "01",
            cma_evlu_amt_icld_yn: str = "Y",
            ovrs_icld_yn: str = "Y") -> Optional[Any]:

        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
            "ORD_UNPR": ord_unpr,
            "ORD_DVSN": ord_dvsn,
            "CMA_EVLU_AMT_ICLD_YN": cma_evlu_amt_icld_yn,
            "OVRS_ICLD_YN": ovrs_icld_yn
        })

        self._headers["tr_id"] = "VTTC8908R" if self._credential.is_demo_account else "TTTC8908R"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=TRADING_INQUIRE_PSBL_ORDER_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_trading_inquire_psbl_sell_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str,
            pdno: str) -> Optional[Any]:

        self._ensure_credentials()
        if self._credential.is_demo_account:
            raise ValueError("Unsupported for demo account!")

        self._ensure_access_token()

        parameters = dict({
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
        })

        self._headers["tr_id"] = "TTTC8408R"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=TRADING_INQUIRE_PSBL_SELL_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_quotations_price_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode,
            fid_input_iscd: str) -> Optional[Any]:
        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code.value,
            "FID_INPUT_ISCD": fid_input_iscd
        })

        self._headers["tr_id"] = "FHKST01010100" if self._credential.is_demo_account else "FHKST01010100"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_PRICE_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_quotations_price_2_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode,
            fid_input_iscd: str) -> Optional[Any]:
        self._ensure_credentials()
        if self._credential.is_demo_account:
            raise ValueError("Unsupported for demo account!")

        self._ensure_access_token()

        parameters = dict({
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code.value,
            "FID_INPUT_ISCD": fid_input_iscd
        })

        self._headers["tr_id"] = "FHPST01010000"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_PRICE_2_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_quotations_inquire_ccnl_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode,
            fid_input_iscd: str) -> Optional[Any]:
        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code.value,
            "FID_INPUT_ISCD": fid_input_iscd
        })

        self._headers["tr_id"] = "FHKST01010300" if self._credential.is_demo_account else "FHKST01010300"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_CCNL_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    '''
        분류: [국내주식] 업종/기타
        역할: 주식현재가 일자별
    '''
    async def get_quotations_inquire_daily_price_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode,
            fid_input_iscd: str,
            fid_period_div_code: KoreaInvestmentSecuritiesDomesticStockFidPeriodDivCd,
            fid_org_adj_prc: str) -> Optional[Any]:
        self._ensure_credentials()

        parameters = dict({
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code.value,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_PERIOD_DIV_CODE": fid_period_div_code.value,
            "FID_ORG_ADJ_PRC": fid_org_adj_prc
        })

        self._headers["tr_id"] = "FHKST01010400" if self._credential.is_demo_account else "FHKST01010400"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_DAILY_PRICE_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_quotations_inquire_time_itemchartprice_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode,
            fid_input_iscd: str,
            fid_input_hour_1: str,
            fid_pw_data_incu_yn: str,
            fid_etc_cls_code: str) -> Optional[Any]:
        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code.value,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
            "FID_PW_DATA_INCU_YN": fid_pw_data_incu_yn,
            "FID_ETC_CLS_CODE": fid_etc_cls_code
        })

        self._headers["tr_id"] = "FHKST03010200" if self._credential.is_demo_account else "FHKST03010200"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_TIME_ITEMCHARTPRICE_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_quotations_inquire_time_dailychartprice_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode,
            fid_input_iscd: str,
            fid_input_hour_1: str,
            fid_input_date_1: str,
            fid_pw_data_incu_yn: str,
            fid_etc_cls_code: str) -> Optional[Any]:
        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code.value,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_PW_DATA_INCU_YN": fid_pw_data_incu_yn,
            "FID_ETC_CLS_CODE": fid_etc_cls_code
        })

        self._headers["tr_id"] = "FHKST03010200" if self._credential.is_demo_account else "FHKST03010200"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_TIME_DAILYCHARTPRICE_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    '''
        분류: [국내주식] 업종/기타
        역할: 국내휴장일조회
    '''

    async def get_quotations_chk_holiday_v1_async(
            self,
            bass_dt: str) -> Optional[Any]:
        self._ensure_credentials()
        # self._ensure_access_token()

        parameters = dict({
            "BASS_DT": bass_dt,
            "CTX_AREA_NK": "",
            "CTX_AREA_FK": ""
        })

        self._headers["tr_id"] = "CTCA0903R"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_CHK_HOLIDAY_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    '''
        분류: [국내주식] 순위분석
        역할: 국내주식 시가총액 상위
    '''

    async def get_ranking_market_cap_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode,
            fid_div_cls_code: KoreaInvestmentSecuritiesDomesticStockFidDivClsCode,
            fid_input_iscd: KoreaInvestmentSecuritiesDomesticStockFidInputIscd) -> Optional[Any]:
        self._ensure_credentials()
        if self._credential.is_demo_account:
            raise ValueError("Unsupported for demo account!")

        # self._ensure_access_token()

        if fid_cond_mrkt_div_code == KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode.UN:
            raise ValueError("Unified market is not supported!")

        parameters = dict({
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code.value,
            "fid_cond_scr_div_code": "20174",
            "fid_div_cls_code": fid_div_cls_code.value,
            "fid_input_iscd": fid_input_iscd.value,
            "fid_trgt_cls_code": "0",
            "fid_trgt_exls_cls_code": "0",
            "fid_input_price_2": "",
            "fid_input_price_1": "",
            "fid_vol_cnt": "",
        })

        self._headers["tr_id"] = "FHPST01740000"

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=RANKING_MARKET_CAP_V1,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise
