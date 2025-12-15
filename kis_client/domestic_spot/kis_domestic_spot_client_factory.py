from typing import Optional

from kis_client.domestic_spot.clients.kis_domestic_spot_client import KoreaInvestmentSecuritiesSpotClient
from kis_client.domestic_spot.clients.kis_domestic_spot_private_rest_client import \
    KoreaInvestmentSecuritiesSpotPrivateRestClient
from kis_client.domestic_spot.clients.kis_domestic_spot_private_websocket_client import \
    KoreaInvestmentSecuritiesDomesticSpotPrivateWebsocketClient
from kis_client.domestic_spot.clients.kis_domestic_spot_public_rest_client import \
    KoreaInvestmentSecuritiesDomesticSpotPublicRestClient
from kis_client.domestic_spot.clients.kis_domestic_spot_public_websocket_client import \
    KoreaInvestmentSecuritiesDomesticSpotPublicWebsocketClient
from kis_client.domestic_spot.core.kis_domestic_spot_api_call_executor import \
    KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor
from kis_client.domestic_spot.core.kis_domestic_spot_websocket_connector import \
    KoreaInvestmentSecuritiesDomesticSpotWebsocketConnector


class KoreaInvestmentSecuritiesSpotClientFactory:
    def __init__(self):
        pass

    def create_client(self,
                      use_single_process_rate_limiter: Optional[bool] = True,
                      use_inter_process_rate_limiter: Optional[bool] = False) -> KoreaInvestmentSecuritiesSpotClient:
        executor = KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor(
            use_single_process_rate_limiter=use_single_process_rate_limiter,
            use_inter_process_rate_limiter=use_inter_process_rate_limiter)
        public_rest_client = KoreaInvestmentSecuritiesDomesticSpotPublicRestClient(executor=executor)
        private_rest_client = KoreaInvestmentSecuritiesSpotPrivateRestClient(executor=executor)

        connector = KoreaInvestmentSecuritiesDomesticSpotWebsocketConnector()
        public_web_socket_client = KoreaInvestmentSecuritiesDomesticSpotPublicWebsocketClient(connector=connector)
        private_web_socket_client = KoreaInvestmentSecuritiesDomesticSpotPrivateWebsocketClient(connector=connector)

        return KoreaInvestmentSecuritiesSpotClient(executor=executor,
                                                   public_rest_client=public_rest_client,
                                                   private_rest_client=private_rest_client,
                                                   public_websocket_client=public_web_socket_client,
                                                   private_websocket_client=private_web_socket_client)
