from enum import Enum


class KoreaInvestmentSecuritiesDomesticStockCandlestickInterval(Enum):
    OneSecond: str = "1s"
    OneMinute: str = "1m"
    ThreeMinutes: str = "3m"
    FiveMinutes: str = "5m"
    FifteenMinutes: str = "15m"
    ThirtyMinutes: str = "30m"
    OneHour: str = "1h"
    TwoHours: str = "2h"
    FourHours: str = "4h"
    SixHours: str = "6h"
    EightHours: str = "8h"
    TwelveHours: str = "12h"
    OneDay: str = "1d"
    ThreeDays: str = "3d"
    OneWeek: str = "1w"
    OneMonth: str = "1M"
