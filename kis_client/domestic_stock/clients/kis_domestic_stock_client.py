from typing import Optional

from kis_client.domestic_stock.clients.kis_domestic_stock_private_websocket_client import \
    KoreaInvestmentSecuritiesDomesticStockPrivateWebsocketClient
from kis_client.domestic_stock.clients.kis_domestic_stock_public_websocket_client import \
    KoreaInvestmentSecuritiesDomesticStockPublicWebsocketClient
from kis_client.domestic_stock.clients.kis_domestic_stock_rest_client import \
    KoreaInvestmentSecuritiesDomesticStockRestClient
from kis_client.domestic_stock.models.kis_domestic_stock_credentials import \
    KoreaInvestmentSecuritiesDomesticStockCredentials


class KoreaInvestmentSecuritiesDomesticStockClient:
    def __init__(self,
                 rest_client: KoreaInvestmentSecuritiesDomesticStockRestClient,
                 public_websocket_client: KoreaInvestmentSecuritiesDomesticStockPublicWebsocketClient,
                 private_websocket_client: KoreaInvestmentSecuritiesDomesticStockPrivateWebsocketClient):
        self._credential: Optional[KoreaInvestmentSecuritiesDomesticStockCredentials] = None
        self.rest_client = rest_client
        self.public_websocket_client = public_websocket_client
        self.private_websocket_client = private_websocket_client

    async def set_credentials_async(self,
                                    credentials: KoreaInvestmentSecuritiesDomesticStockCredentials):
        self.rest_client.set_credentials(credentials=credentials)
