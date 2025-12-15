from typing import Optional, Any

from kis_client.domestic_spot.clients.kis_domestic_spot_private_rest_client import \
    KoreaInvestmentSecuritiesSpotPrivateRestClient
from kis_client.domestic_spot.clients.kis_domestic_spot_private_websocket_client import \
    KoreaInvestmentSecuritiesDomesticSpotPrivateWebsocketClient
from kis_client.domestic_spot.clients.kis_domestic_spot_public_rest_client import \
    KoreaInvestmentSecuritiesDomesticSpotPublicRestClient
from kis_client.domestic_spot.clients.kis_domestic_spot_public_websocket_client import \
    KoreaInvestmentSecuritiesDomesticSpotPublicWebsocketClient
from kis_client.domestic_spot.constants.kis_spot_endpoints import *
from kis_client.domestic_spot.core.kis_domestic_spot_api_call_executor import \
    KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor
from kis_client.domestic_spot.models.kis_domestic_spot_credentials import \
    KoreaInvestmentSecuritiesDomesticSpotCredentials


class KoreaInvestmentSecuritiesSpotClient:
    def __init__(self,
                 executor: KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor,
                 public_rest_client: KoreaInvestmentSecuritiesDomesticSpotPublicRestClient,
                 private_rest_client: KoreaInvestmentSecuritiesSpotPrivateRestClient,
                 public_websocket_client: KoreaInvestmentSecuritiesDomesticSpotPublicWebsocketClient,
                 private_websocket_client: KoreaInvestmentSecuritiesDomesticSpotPrivateWebsocketClient):
        self._credential: Optional[KoreaInvestmentSecuritiesDomesticSpotCredentials] = None
        self._executor = executor
        self.public_rest_client = public_rest_client
        self.private_rest_client = private_rest_client
        self.public_websocket_client = public_websocket_client
        self.private_websocket_client = private_websocket_client

    def set_credentials(self,
                        credentials: KoreaInvestmentSecuritiesDomesticSpotCredentials):
        self.public_rest_client.set_credentials(credentials=credentials)
        self.private_rest_client.set_credentials(credentials=credentials)

    def set_access_token(self,
                         access_token: str):
        self.public_rest_client.set_access_token(access_token=access_token)
        self.private_rest_client.set_access_token(access_token=access_token)

    def _ensure_credentials(self):
        if self._credential is None:
            raise ValueError("Please set credentials!")

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
            data = await self._executor.execute_rest_api_call_async(http_method="post",
                                                                    endpoint=OAUTH2_TOKEN_P,
                                                                    headers=headers,
                                                                    parameters=parameters)
            return data
        except Exception:
            raise
