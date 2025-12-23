from typing import Optional

from kis_client.domestic_stock.clients.kis_domestic_stock_private_websocket_client import \
    KoreaInvestmentSecuritiesDomesticStockPrivateWebsocketClient
from kis_client.domestic_stock.clients.kis_domestic_stock_public_websocket_client import \
    KoreaInvestmentSecuritiesDomesticStockPublicWebsocketClient
from kis_client.domestic_stock.clients.kis_domestic_stock_rest_client import \
    KoreaInvestmentSecuritiesDomesticStockRestClient
from kis_client.domestic_stock.core.kis_domestic_stock_access_token_manager import \
    KoreaInvestmentSecuritiesDomesticStockAccessTokenManager
from kis_client.domestic_stock.models.kis_domestic_stock_credentials import \
    KoreaInvestmentSecuritiesDomesticStockCredentials


class KoreaInvestmentSecuritiesDomesticStockClient:
    def __init__(self,
                 rest_client: KoreaInvestmentSecuritiesDomesticStockRestClient,
                 public_websocket_client: KoreaInvestmentSecuritiesDomesticStockPublicWebsocketClient,
                 private_websocket_client: KoreaInvestmentSecuritiesDomesticStockPrivateWebsocketClient,
                 access_token_manager: KoreaInvestmentSecuritiesDomesticStockAccessTokenManager):
        self._credential: Optional[KoreaInvestmentSecuritiesDomesticStockCredentials] = None
        self.rest_client = rest_client
        self.public_websocket_client = public_websocket_client
        self.private_websocket_client = private_websocket_client
        self.access_token_manager = access_token_manager

    async def set_credentials_async(self,
                                    credentials: KoreaInvestmentSecuritiesDomesticStockCredentials):
        self.rest_client.set_credentials(credentials=credentials)
        self.access_token_manager.set_credentials(credentials=credentials)

        access_token = await self.access_token_manager.get_access_token_async(public_key=credentials.public_key)
        self._set_access_token(access_token=access_token)

    def _set_access_token(self,
                          access_token: str):
        self.rest_client.set_access_token(access_token=access_token)
