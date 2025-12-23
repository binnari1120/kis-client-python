from typing import Optional

from kis_client.domestic_stock.clients.kis_domestic_stock_client import KoreaInvestmentSecuritiesDomesticStockClient
from kis_client.domestic_stock.clients.kis_domestic_stock_private_rest_client import \
    KoreaInvestmentSecuritiesStockPrivateRestClient
from kis_client.domestic_stock.clients.kis_domestic_stock_private_websocket_client import \
    KoreaInvestmentSecuritiesDomesticStockPrivateWebsocketClient
from kis_client.domestic_stock.clients.kis_domestic_stock_public_rest_client import \
    KoreaInvestmentSecuritiesDomesticStockPublicRestClient
from kis_client.domestic_stock.clients.kis_domestic_stock_public_websocket_client import \
    KoreaInvestmentSecuritiesDomesticStockPublicWebsocketClient
from kis_client.domestic_stock.core.kis_domestic_stock_api_call_executor import \
    KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor
from kis_client.domestic_stock.core.kis_domestic_stock_websocket_connector import \
    KoreaInvestmentSecuritiesDomesticStockWebsocketConnector


class KoreaInvestmentSecuritiesDomesticStockClientFactory:
    def __init__(self):
        pass

    def create_client(self,
                      use_single_process_rate_limiter: Optional[bool] = True,
                      use_inter_process_rate_limiter: Optional[bool] = False) -> KoreaInvestmentSecuritiesDomesticStockClient:
        executor = KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor(
            use_single_process_rate_limiter=use_single_process_rate_limiter,
            use_inter_process_rate_limiter=use_inter_process_rate_limiter)
        public_rest_client = KoreaInvestmentSecuritiesDomesticStockPublicRestClient(executor=executor)
        private_rest_client = KoreaInvestmentSecuritiesStockPrivateRestClient(executor=executor)

        connector = KoreaInvestmentSecuritiesDomesticStockWebsocketConnector()
        public_web_socket_client = KoreaInvestmentSecuritiesDomesticStockPublicWebsocketClient(connector=connector)
        private_web_socket_client = KoreaInvestmentSecuritiesDomesticStockPrivateWebsocketClient(connector=connector)

        return KoreaInvestmentSecuritiesDomesticStockClient(executor=executor,
                                                            public_rest_client=public_rest_client,
                                                            private_rest_client=private_rest_client,
                                                            public_websocket_client=public_web_socket_client,
                                                            private_websocket_client=private_web_socket_client)
