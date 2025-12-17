from typing import Optional, Any, Union

from kis_client.domestic_spot.constants.kis_spot_endpoints import *
from kis_client.domestic_spot.core.kis_domestic_spot_api_call_executor import \
    KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor
from kis_client.domestic_spot.enums.kis_domestic_spot_afhr_flpr_yn import \
    KoreaInvestmentSecuritiesDomesticSpotAfhrFlprYn
from kis_client.domestic_spot.enums.kis_domestic_spot_excg_id_dvsn_cd import \
    KoreaInvestmentSecuritiesDomesticSpotExcgIdDvsnCd
from kis_client.domestic_spot.models.kis_domestic_spot_credentials import \
    KoreaInvestmentSecuritiesDomesticSpotCredentials


class KoreaInvestmentSecuritiesSpotPrivateRestClient:
    RECV_WINDOW = 50000

    def __init__(self, executor: KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor):
        self._credential: Optional[KoreaInvestmentSecuritiesDomesticSpotCredentials] = None
        self._executor = executor

    def set_credentials(self,
                        credentials: KoreaInvestmentSecuritiesDomesticSpotCredentials):
        self._credential = credentials

    def set_access_token(self,
                         access_token: str):
        self._access_token = access_token

    def _ensure_credentials(self):
        if self._credential is None:
            raise ValueError("Please set credentials!")

    def _ensure_access_token(self):
        if self._access_token is None:
            raise ValueError("Please set access token!")

    async def get_token_async(self) -> Optional[Any]:
        self._ensure_credentials()

        parameters = dict({
            "grant_type": "client_credentials",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key
        })

        headers = {
            # "content-type": "application/json; charset=utf-8",
            "content-type": "application/x-www-form-urlencoded",
        }

        try:
            data = await self._executor.execute_public_api_call_async(http_method="post",
                                                                      endpoint=OAUTH2_TOKEN_P,
                                                                      headers=headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

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
                                                   KoreaInvestmentSecuritiesDomesticSpotExcgIdDvsnCd] = None):
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

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": tr_id,
            # "seq_no": "001" if self._credential.is_corporate_account else None,
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_private_api_call_async(http_method="post",
                                                                       endpoint=TRADING_ORDER_CASH_V1,
                                                                       headers=headers,
                                                                       parameters=parameters)
            return data
        except Exception:
            raise

    async def get_trading_inquire_balance_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str,
            afhr_flp_yn: KoreaInvestmentSecuritiesDomesticSpotAfhrFlprYn,
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

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "VTTC8434R" if self._credential.is_demo_account else "TTTC8434R",
            # "seq_no": "001" if self._credential.is_corporate_account else None,
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_private_api_call_async(http_method="get",
                                                                       endpoint=TRADING_INQUIRE_BALANCE_V1,
                                                                       headers=headers,
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

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "TTTC0084R",
            # "seq_no": "001" if self._credential.is_corporate_account else None,
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_private_api_call_async(http_method="get",
                                                                       endpoint=TRADING_INQUIRE_PSBL_RVSECNCL_V1,
                                                                       headers=headers,
                                                                       parameters=parameters)
            return data
        except Exception:
            raise

    async def get_trading_inquire_balance_rlz_pl_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str,
            afhr_flp_yn: KoreaInvestmentSecuritiesDomesticSpotAfhrFlprYn,
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

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "TTTC8494R",
            # "seq_no": "001" if self._credential.is_corporate_account else None,
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_private_api_call_async(http_method="get",
                                                                       endpoint=TRADING_INQUIRE_BALANCE_RLZ_PL_V1,
                                                                       headers=headers,
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

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "TTTC8408R",
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=TRADING_INQUIRE_PSBL_SELL_V1,
                                                                      headers=headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_trading_order_resv_ccnl_v1_async(
            self,
            cano: str,
            acnt_prdt_cd: str,
            afhr_flp_yn: KoreaInvestmentSecuritiesDomesticSpotAfhrFlprYn,
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

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "CTSC0004R",
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=TRADING_ORDER_RESV_CCNL_V1,
                                                                      headers=headers,
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

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "CTRP6548R",
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=TRADING_INQUIRE_ACCOUNT_BALANCE_V1,
                                                                      headers=headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise
