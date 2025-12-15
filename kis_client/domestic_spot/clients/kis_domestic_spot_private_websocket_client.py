from kis_client.domestic_spot.core.kis_domestic_spot_websocket_connector import KoreaInvestmentSecuritiesDomesticSpotWebsocketConnector


class KoreaInvestmentSecuritiesDomesticSpotPrivateWebsocketClient:
    RECV_WINDOW = 50000

    def __init__(self, connector: KoreaInvestmentSecuritiesDomesticSpotWebsocketConnector):
        self._connector = connector
