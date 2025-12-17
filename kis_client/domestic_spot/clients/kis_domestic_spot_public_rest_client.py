from typing import Optional, Any

from kis_client.domestic_spot.constants.kis_spot_endpoints import *
from kis_client.domestic_spot.core.kis_domestic_spot_api_call_executor import \
    KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor
from kis_client.domestic_spot.enums.kis_domestic_spot_fid_cond_mrkt_div_code import \
    KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode
from kis_client.domestic_spot.models.kis_domestic_spot_credentials import \
    KoreaInvestmentSecuritiesDomesticSpotCredentials


class KoreaInvestmentSecuritiesDomesticSpotPublicRestClient:
    RECV_WINDOW = 50000

    def __init__(self, executor: KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor):
        self._credential: Optional[KoreaInvestmentSecuritiesDomesticSpotCredentials] = None
        self._access_token: Optional[str] = None
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

    async def get_quotations_price_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode,
            fid_input_iscd: str) -> Optional[Any]:
        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code.value,
            "FID_INPUT_ISCD": fid_input_iscd
        })

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "FHKST01010100" if self._credential.is_demo_account else "FHKST01010100",
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_PRICE_V1,
                                                                      headers=headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_quotations_price_2_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode,
            fid_input_iscd: str) -> Optional[Any]:
        self._ensure_credentials()
        if self._credential.is_demo_account:
            raise ValueError("Unsupported for demo account!")

        self._ensure_access_token()

        parameters = dict({
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code.value,
            "FID_INPUT_ISCD": fid_input_iscd
        })

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "FHPST01010000",
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_PRICE_2_V1,
                                                                      headers=headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_quotations_ccnl_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode,
            fid_input_iscd: str) -> Optional[Any]:
        self._ensure_credentials()
        self._ensure_access_token()

        parameters = dict({
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code.value,
            "FID_INPUT_ISCD": fid_input_iscd
        })

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "FHKST01010300" if self._credential.is_demo_account else "FHKST01010300",
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_CCNL_V1,
                                                                      headers=headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_quotations_inquire_time_itemchartprice_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode,
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

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "FHKST03010200" if self._credential.is_demo_account else "FHKST03010200",
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_TIME_ITEMCHARTPRICE_V1,
                                                                      headers=headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise

    async def get_quotations_inquire_time_dailychartprice_v1_async(
            self,
            fid_cond_mrkt_div_code: KoreaInvestmentSecuritiesDomesticSpotFidCondMrktDivCode,
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

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key,
            "tr_id": "FHKST03010200" if self._credential.is_demo_account else "FHKST03010200",
            "custtype": "B" if self._credential.is_corporate_account else "P",
        }

        try:
            data = await self._executor.execute_public_api_call_async(http_method="get",
                                                                      endpoint=QUOTATIONS_INQUIRE_TIME_DAILYCHARTPRICE_V1,
                                                                      headers=headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise
