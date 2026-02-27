from kis_client.domestic_stock.core.kis_domestic_stock_websocket_connector import \
    KoreaInvestmentSecuritiesDomesticStockWebsocketConnector


class KoreaInvestmentSecuritiesDomesticStockPrivateWebsocketClient:
    RECV_WINDOW = 50000

    def __init__(self, connector: KoreaInvestmentSecuritiesDomesticStockWebsocketConnector):
        self._connector = connector
