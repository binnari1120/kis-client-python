from datetime import datetime, timezone, timedelta
from typing import Any
from typing import Optional

import keyring

from kis_client.domestic_stock.constants.kis_domestic_stock_endpoints import *
from kis_client.domestic_stock.core.kis_domestic_stock_api_call_executor import \
    KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor
from kis_client.domestic_stock.models.kis_domestic_stock_credentials import \
    KoreaInvestmentSecuritiesDomesticStockCredentials


class KoreaInvestmentSecuritiesDomesticStockAccessTokenManager:
    SERVICE_NAME = "KIS-CLIENT"

    def __init__(self, executor: KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor):
        self._credential: Optional[KoreaInvestmentSecuritiesDomesticStockCredentials] = None
        self._executor = executor
        self._headers = {
            # "content-type": "application/json; charset=utf-8",
            "content-type": "application/x-www-form-urlencoded",
        }

    def set_credentials(self,
                        credentials: KoreaInvestmentSecuritiesDomesticStockCredentials):
        self._credential = credentials

    def set_access_token(self,
                         access_token: str):
        self._access_token = access_token

    def _ensure_credentials(self):
        if self._credential is None:
            raise ValueError("Please set credentials!")

    def _is_expired(self,
                    expiration: str) -> bool:
        if not expiration:
            return True
        tz_info = timezone(timedelta(hours=9))
        current_kst_date = datetime.now().replace(tzinfo=tz_info)
        expiration_date = datetime.fromisoformat(expiration)
        if expiration_date.tzinfo is None:
            expiration_date = expiration_date.replace(tzinfo=tz_info)
        return expiration_date <= current_kst_date

    def _set_access_token(self,
                          public_key: str,
                          access_token: str,
                          expiration: str):
        keyring.set_password(self.SERVICE_NAME, f"{public_key}:access_token", access_token)
        keyring.set_password(self.SERVICE_NAME, f"{public_key}:expiration", expiration)

    async def get_access_token_async(self, public_key: str) -> str:
        access_token = keyring.get_password(self.SERVICE_NAME, f"{public_key}:access_token")
        expiration = keyring.get_password(self.SERVICE_NAME, f"{public_key}:expiration")

        if not access_token or self._is_expired(expiration=expiration):
            print("토큰 없음 → 신규 발급 중 ...")
            token_details = await self.post_oauth2_token_async()
            print(token_details)
            self._set_access_token(public_key=public_key,
                                   access_token=token_details["access_token"],
                                   expiration=token_details["access_token_token_expired"])
        return access_token

    async def post_oauth2_token_async(self) -> Optional[Any]:
        self._ensure_credentials()

        parameters = dict({
            "grant_type": "client_credentials",
            "appkey": self._credential.public_key,
            "appsecret": self._credential.private_key
        })

        try:
            data = await self._executor.execute_public_api_call_async(http_method="post",
                                                                      endpoint=OAUTH2_TOKEN_P,
                                                                      headers=self._headers,
                                                                      parameters=parameters)
            return data
        except Exception:
            raise
