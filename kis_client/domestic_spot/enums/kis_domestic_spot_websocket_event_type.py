from enum import Enum


class KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType(Enum):
    Unidentified: str = "unidentified"
    MarkPriceUpdate: str = "markPriceUpdate"
    Kline: str = "kline"
    Ticker: str = "24hrTicker"
    DepthUpdate: str = "depthUpdate"
    AccountUpdate: str = "ACCOUNT_UPDATE"
    OrderTradeUpdate: str = "ORDER_TRADE_UPDATE"
    AccountConfigurationUpdate: str = "ACCOUNT_CONFIG_UPDATE"
    StrategyUpdate: str = "STRATEGY_UPDATE"
    GridUpdate: str = "GRID_UPDATE"
    ConditionalOrderTriggerReject: str = "CONDITIONAL_ORDER_TRIGGER_REJECT"
