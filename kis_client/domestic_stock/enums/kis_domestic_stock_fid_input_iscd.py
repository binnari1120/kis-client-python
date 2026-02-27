from enum import Enum


class KoreaInvestmentSecuritiesDomesticStockFidInputIscd(Enum):
    All = "00000"  # 전체
    Krx = "0001"  # 거래소
    Kosdaq = "1001"  # 코스닥
    Kosfi200 = "2001"  # 코스피200
