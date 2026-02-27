import pathlib

import pytest
import yaml

from kis_client.domestic_stock.enums.kis_domestic_stock_fid_cond_mrkt_div_code import \
    KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode
from kis_client.domestic_stock.enums.kis_domestic_stock_fid_div_cls_code import \
    KoreaInvestmentSecuritiesDomesticStockFidDivClsCode
from kis_client.domestic_stock.enums.kis_domestic_stock_fid_input_iscd import \
    KoreaInvestmentSecuritiesDomesticStockFidInputIscd
from kis_client.domestic_stock.kis_domestic_stock_client_factory import \
    KoreaInvestmentSecuritiesDomesticStockClientFactory
from kis_client.domestic_stock.models.kis_domestic_stock_credentials import \
    KoreaInvestmentSecuritiesDomesticStockCredentials

factory = KoreaInvestmentSecuritiesDomesticStockClientFactory()
client = factory.create_client()


@pytest.mark.asyncio
async def test_set_credentials():
    with open(f"{pathlib.Path(__file__).parent.parent.parent}/configurations/accounts.yaml", "r",
              encoding="utf-8") as file:
        accounts = yaml.safe_load(file)

    account = accounts["Spot"]
    public_key = account.get("public_key", "")
    private_key = account.get("private_key", "")
    if not public_key:
        raise Exception("Empty value: public_key")
    elif not private_key:
        raise Exception("Empty value: private_key")

    credentials = KoreaInvestmentSecuritiesDomesticStockCredentials(public_key=accounts["Spot"]["public_key"],
                                                                    private_key=accounts["Spot"]["private_key"])
    await client.set_credentials_async(credentials=credentials)


@pytest.mark.asyncio
async def test_get_ranking_market_cap_v1_async():
    # {
    #     "output": [
    #         {
    #             "mksc_shrn_iscd": "005930",
    #             "data_rank": "1",
    #             "hts_kor_isnm": "삼성전자",
    #             "stck_prpr": "128500",
    #             "prdy_vrss": "8600",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "7.17",
    #             "acml_vol": "30463279",
    #             "lstn_stcn": "5919637922",
    #             "stck_avls": "7606735",
    #             "mrkt_whol_avls_rlim": "17.31"
    #         },
    #         {
    #             "mksc_shrn_iscd": "000660",
    #             "data_rank": "2",
    #             "hts_kor_isnm": "SK하이닉스",
    #             "stck_prpr": "677000",
    #             "prdy_vrss": "26000",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "3.99",
    #             "acml_vol": "4181895",
    #             "lstn_stcn": "728002365",
    #             "stck_avls": "4928576",
    #             "mrkt_whol_avls_rlim": "11.22"
    #         },
    #         {
    #             "mksc_shrn_iscd": "373220",
    #             "data_rank": "3",
    #             "hts_kor_isnm": "LG에너지솔루션",
    #             "stck_prpr": "361000",
    #             "prdy_vrss": "-7500",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-2.04",
    #             "acml_vol": "329529",
    #             "lstn_stcn": "234000000",
    #             "stck_avls": "844740",
    #             "mrkt_whol_avls_rlim": "1.92"
    #         },
    #         {
    #             "mksc_shrn_iscd": "207940",
    #             "data_rank": "4",
    #             "hts_kor_isnm": "삼성바이오로직스",
    #             "stck_prpr": "1683000",
    #             "prdy_vrss": "-12000",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-0.71",
    #             "acml_vol": "46684",
    #             "lstn_stcn": "46290951",
    #             "stck_avls": "779077",
    #             "mrkt_whol_avls_rlim": "1.77"
    #         },
    #         {
    #             "mksc_shrn_iscd": "005380",
    #             "data_rank": "5",
    #             "hts_kor_isnm": "현대차",
    #             "stck_prpr": "298500",
    #             "prdy_vrss": "2000",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "0.67",
    #             "acml_vol": "955205",
    #             "lstn_stcn": "204757766",
    #             "stck_avls": "611202",
    #             "mrkt_whol_avls_rlim": "1.39"
    #         },
    #         {
    #             "mksc_shrn_iscd": "329180",
    #             "data_rank": "6",
    #             "hts_kor_isnm": "HD현대중공업",
    #             "stck_prpr": "504000",
    #             "prdy_vrss": "-5000",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-0.98",
    #             "acml_vol": "225977",
    #             "lstn_stcn": "104961225",
    #             "stck_avls": "529005",
    #             "mrkt_whol_avls_rlim": "1.20"
    #         },
    #         {
    #             "mksc_shrn_iscd": "402340",
    #             "data_rank": "7",
    #             "hts_kor_isnm": "SK스퀘어",
    #             "stck_prpr": "392000",
    #             "prdy_vrss": "24000",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "6.52",
    #             "acml_vol": "423146",
    #             "lstn_stcn": "132087115",
    #             "stck_avls": "517781",
    #             "mrkt_whol_avls_rlim": "1.18"
    #         },
    #         {
    #             "mksc_shrn_iscd": "012450",
    #             "data_rank": "8",
    #             "hts_kor_isnm": "한화에어로스페이스",
    #             "stck_prpr": "946000",
    #             "prdy_vrss": "5000",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "0.53",
    #             "acml_vol": "144603",
    #             "lstn_stcn": "51563401",
    #             "stck_avls": "487790",
    #             "mrkt_whol_avls_rlim": "1.11"
    #         },
    #         {
    #             "mksc_shrn_iscd": "034020",
    #             "data_rank": "9",
    #             "hts_kor_isnm": "두산에너빌리티",
    #             "stck_prpr": "75200",
    #             "prdy_vrss": "-100",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-0.13",
    #             "acml_vol": "2800553",
    #             "lstn_stcn": "640561146",
    #             "stck_avls": "481702",
    #             "mrkt_whol_avls_rlim": "1.10"
    #         },
    #         {
    #             "mksc_shrn_iscd": "000270",
    #             "data_rank": "10",
    #             "hts_kor_isnm": "기아",
    #             "stck_prpr": "120600",
    #             "prdy_vrss": "-1200",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-0.99",
    #             "acml_vol": "645645",
    #             "lstn_stcn": "390412998",
    #             "stck_avls": "470838",
    #             "mrkt_whol_avls_rlim": "1.07"
    #         },
    #         {
    #             "mksc_shrn_iscd": "105560",
    #             "data_rank": "11",
    #             "hts_kor_isnm": "KB금융",
    #             "stck_prpr": "123300",
    #             "prdy_vrss": "-1400",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-1.12",
    #             "acml_vol": "648227",
    #             "lstn_stcn": "381462103",
    #             "stck_avls": "470343",
    #             "mrkt_whol_avls_rlim": "1.07"
    #         },
    #         {
    #             "mksc_shrn_iscd": "068270",
    #             "data_rank": "12",
    #             "hts_kor_isnm": "셀트리온",
    #             "stck_prpr": "202500",
    #             "prdy_vrss": "21500",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "11.88",
    #             "acml_vol": "3440514",
    #             "lstn_stcn": "230960969",
    #             "stck_avls": "467696",
    #             "mrkt_whol_avls_rlim": "1.06"
    #         },
    #         {
    #             "mksc_shrn_iscd": "028260",
    #             "data_rank": "13",
    #             "hts_kor_isnm": "삼성물산",
    #             "stck_prpr": "245000",
    #             "prdy_vrss": "5500",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "2.30",
    #             "acml_vol": "360079",
    #             "lstn_stcn": "169976544",
    #             "stck_avls": "416443",
    #             "mrkt_whol_avls_rlim": "0.95"
    #         },
    #         {
    #             "mksc_shrn_iscd": "035420",
    #             "data_rank": "14",
    #             "hts_kor_isnm": "NAVER",
    #             "stck_prpr": "247000",
    #             "prdy_vrss": "4500",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "1.86",
    #             "acml_vol": "1362199",
    #             "lstn_stcn": "156852638",
    #             "stck_avls": "387426",
    #             "mrkt_whol_avls_rlim": "0.88"
    #         },
    #         {
    #             "mksc_shrn_iscd": "055550",
    #             "data_rank": "15",
    #             "hts_kor_isnm": "신한지주",
    #             "stck_prpr": "76600",
    #             "prdy_vrss": "-300",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-0.39",
    #             "acml_vol": "640114",
    #             "lstn_stcn": "485494934",
    #             "stck_avls": "371889",
    #             "mrkt_whol_avls_rlim": "0.85"
    #         },
    #         {
    #             "mksc_shrn_iscd": "042660",
    #             "data_rank": "16",
    #             "hts_kor_isnm": "한화오션",
    #             "stck_prpr": "114700",
    #             "prdy_vrss": "1100",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "0.97",
    #             "acml_vol": "1511307",
    #             "lstn_stcn": "306413394",
    #             "stck_avls": "351456",
    #             "mrkt_whol_avls_rlim": "0.80"
    #         },
    #         {
    #             "mksc_shrn_iscd": "012330",
    #             "data_rank": "17",
    #             "hts_kor_isnm": "현대모비스",
    #             "stck_prpr": "369000",
    #             "prdy_vrss": "-4000",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-1.07",
    #             "acml_vol": "230839",
    #             "lstn_stcn": "90732583",
    #             "stck_avls": "334803",
    #             "mrkt_whol_avls_rlim": "0.76"
    #         },
    #         {
    #             "mksc_shrn_iscd": "032830",
    #             "data_rank": "18",
    #             "hts_kor_isnm": "삼성생명",
    #             "stck_prpr": "156300",
    #             "prdy_vrss": "-1300",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-0.82",
    #             "acml_vol": "266320",
    #             "lstn_stcn": "200000000",
    #             "stck_avls": "312600",
    #             "mrkt_whol_avls_rlim": "0.71"
    #         },
    #         {
    #             "mksc_shrn_iscd": "015760",
    #             "data_rank": "19",
    #             "hts_kor_isnm": "한국전력",
    #             "stck_prpr": "46500",
    #             "prdy_vrss": "-700",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-1.48",
    #             "acml_vol": "2308514",
    #             "lstn_stcn": "641964077",
    #             "stck_avls": "298513",
    #             "mrkt_whol_avls_rlim": "0.68"
    #         },
    #         {
    #             "mksc_shrn_iscd": "267260",
    #             "data_rank": "20",
    #             "hts_kor_isnm": "HD현대일렉트릭",
    #             "stck_prpr": "819000",
    #             "prdy_vrss": "45000",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "5.81",
    #             "acml_vol": "132745",
    #             "lstn_stcn": "36047135",
    #             "stck_avls": "295226",
    #             "mrkt_whol_avls_rlim": "0.67"
    #         },
    #         {
    #             "mksc_shrn_iscd": "009540",
    #             "data_rank": "21",
    #             "hts_kor_isnm": "HD한국조선해양",
    #             "stck_prpr": "393500",
    #             "prdy_vrss": "-13500",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-3.32",
    #             "acml_vol": "256720",
    #             "lstn_stcn": "70773116",
    #             "stck_avls": "278492",
    #             "mrkt_whol_avls_rlim": "0.63"
    #         },
    #         {
    #             "mksc_shrn_iscd": "035720",
    #             "data_rank": "22",
    #             "hts_kor_isnm": "카카오",
    #             "stck_prpr": "62100",
    #             "prdy_vrss": "2000",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "3.33",
    #             "acml_vol": "2903206",
    #             "lstn_stcn": "442423799",
    #             "stck_avls": "274745",
    #             "mrkt_whol_avls_rlim": "0.63"
    #         },
    #         {
    #             "mksc_shrn_iscd": "086790",
    #             "data_rank": "23",
    #             "hts_kor_isnm": "하나금융지주",
    #             "stck_prpr": "93400",
    #             "prdy_vrss": "-700",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-0.74",
    #             "acml_vol": "470548",
    #             "lstn_stcn": "278325814",
    #             "stck_avls": "259956",
    #             "mrkt_whol_avls_rlim": "0.59"
    #         },
    #         {
    #             "mksc_shrn_iscd": "196170",
    #             "data_rank": "24",
    #             "hts_kor_isnm": "알테오젠",
    #             "stck_prpr": "457000",
    #             "prdy_vrss": "7500",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "1.67",
    #             "acml_vol": "374917",
    #             "lstn_stcn": "53505788",
    #             "stck_avls": "244521",
    #             "mrkt_whol_avls_rlim": "0.56"
    #         },
    #         {
    #             "mksc_shrn_iscd": "005490",
    #             "data_rank": "25",
    #             "hts_kor_isnm": "POSCO홀딩스",
    #             "stck_prpr": "297500",
    #             "prdy_vrss": "-7500",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-2.46",
    #             "acml_vol": "424246",
    #             "lstn_stcn": "80932952",
    #             "stck_avls": "240776",
    #             "mrkt_whol_avls_rlim": "0.55"
    #         },
    #         {
    #             "mksc_shrn_iscd": "010130",
    #             "data_rank": "26",
    #             "hts_kor_isnm": "고려아연",
    #             "stck_prpr": "1287000",
    #             "prdy_vrss": "-29000",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-2.20",
    #             "acml_vol": "38628",
    #             "lstn_stcn": "18663253",
    #             "stck_avls": "240196",
    #             "mrkt_whol_avls_rlim": "0.55"
    #         },
    #         {
    #             "mksc_shrn_iscd": "000810",
    #             "data_rank": "27",
    #             "hts_kor_isnm": "삼성화재",
    #             "stck_prpr": "497000",
    #             "prdy_vrss": "0",
    #             "prdy_vrss_sign": "3",
    #             "prdy_ctrt": "0.00",
    #             "acml_vol": "40982",
    #             "lstn_stcn": "46011155",
    #             "stck_avls": "228675",
    #             "mrkt_whol_avls_rlim": "0.52"
    #         },
    #         {
    #             "mksc_shrn_iscd": "051910",
    #             "data_rank": "28",
    #             "hts_kor_isnm": "LG화학",
    #             "stck_prpr": "322500",
    #             "prdy_vrss": "-10500",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-3.15",
    #             "acml_vol": "246623",
    #             "lstn_stcn": "70592343",
    #             "stck_avls": "227660",
    #             "mrkt_whol_avls_rlim": "0.52"
    #         },
    #         {
    #             "mksc_shrn_iscd": "010140",
    #             "data_rank": "29",
    #             "hts_kor_isnm": "삼성중공업",
    #             "stck_prpr": "24150",
    #             "prdy_vrss": "50",
    #             "prdy_vrss_sign": "2",
    #             "prdy_ctrt": "0.21",
    #             "acml_vol": "3718965",
    #             "lstn_stcn": "880000000",
    #             "stck_avls": "212520",
    #             "mrkt_whol_avls_rlim": "0.48"
    #         },
    #         {
    #             "mksc_shrn_iscd": "006400",
    #             "data_rank": "30",
    #             "hts_kor_isnm": "삼성SDI",
    #             "stck_prpr": "262500",
    #             "prdy_vrss": "-7000",
    #             "prdy_vrss_sign": "5",
    #             "prdy_ctrt": "-2.60",
    #             "acml_vol": "616243",
    #             "lstn_stcn": "80585530",
    #             "stck_avls": "211537",
    #             "mrkt_whol_avls_rlim": "0.48"
    #         }
    #     ],
    #     "rt_cd": "0",
    #     "msg_cd": "MCA00000",
    #     "msg1": "정상처리 되었습니다."
    # }
    
    fid_cond_mrkt_div_code = KoreaInvestmentSecuritiesDomesticStockFidCondMrktDivCode.J
    fid_div_cls_code = KoreaInvestmentSecuritiesDomesticStockFidDivClsCode.Common
    fid_input_iscd = KoreaInvestmentSecuritiesDomesticStockFidInputIscd.All

    ranking_details = await client.rest_client.get_ranking_market_cap_v1_async(
        fid_cond_mrkt_div_code=fid_cond_mrkt_div_code,
        fid_div_cls_code=fid_div_cls_code,
        fid_input_iscd=fid_input_iscd)

    print(f"========== test_get_ranking_market_cap_v1_async ==========")
    assert "output" in ranking_details
    for ranking_detail in ranking_details["output"]:
        assert int(ranking_detail["mksc_shrn_iscd"])

        print(f"{ranking_detail['hts_kor_isnm']} 시가총액: {int(ranking_detail['stck_avls']) / 10000}조")
