import json
from typing import Optional, Any, Literal, Dict

import aiohttp

from kis_client.domestic_spot.constants.kis_spot_hosts import *
from kis_client.domestic_spot.core.kis_domestic_spot_inter_process_rate_limiter import \
    KoreaInvestmentSecuritiesDomesticSpotInterProcessRateLimiter
from kis_client.domestic_spot.core.kis_domestic_spot_single_process_rate_limiter import \
    KoreaInvestmentSecuritiesSpotSingleProcessRateLimiter
from kis_client.domestic_spot.decorators.kis_domestic_spot_inter_process_rate_limited import \
    kis_spot_inter_process_rate_limited
from kis_client.domestic_spot.decorators.kis_domestic_spot_single_process_rate_limited import \
    kis_spot_single_process_rate_limited


class KoreaInvestmentSecuritiesDomesticSpotApiCallExecutor:
    def __init__(self,
                 use_single_process_rate_limiter: bool = False,
                 use_inter_process_rate_limiter: bool = False):
        self._spot_single_process_rate_limiter = KoreaInvestmentSecuritiesSpotSingleProcessRateLimiter() if use_single_process_rate_limiter else None
        self._spot_inter_process_rate_limiter = KoreaInvestmentSecuritiesDomesticSpotInterProcessRateLimiter() if use_inter_process_rate_limiter else None
        if self._spot_inter_process_rate_limiter:
            self._spot_single_process_rate_limiter = None

    def __build_query_string(self, parameters):
        return "&".join([f"{key}={value}" for key, value in parameters.items()])

    @kis_spot_single_process_rate_limited
    @kis_spot_inter_process_rate_limited
    async def execute_public_api_call_async(self,
                                            http_method: Literal["post", "get", "put", "delete"],
                                            endpoint: str,
                                            headers: Dict[str, str],
                                            parameters: Optional[Any] = None):
        request_url = f"{REST_API_HOST}{endpoint}"
        # if parameters is not None:
        #     query_string = self.__build_query_string(parameters=parameters)
        #     request_url += f"?{query_string}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method=http_method.upper(),
                                           url=request_url,
                                           params=parameters if http_method.lower() == "get" else None,
                                           data=json.dumps(parameters) if http_method.lower() != "get" else None,
                                           # data=json.dumps(parameters),
                                           headers=headers) as response:
                    text = await response.json()
                    if response.status == 200 and "application/json" in response.headers.get("Content-Type"):
                        return text

                    try:
                        error_message = json.loads(await response.text())["error_description"]
                        raise ValueError(error_message)
                    except:
                        raise ValueError(text)
            except Exception:
                raise

    @kis_spot_single_process_rate_limited
    @kis_spot_inter_process_rate_limited
    async def execute_private_api_call_async(self,
                                             http_method: Literal["get", "post", "put", "delete"],
                                             endpoint: str,
                                             headers: Dict[str, str],
                                             parameters: dict):
        request_url = f"{REST_API_HOST}{endpoint}"
        # if parameters is not None:
        #     query_string = self.__build_query_string(parameters=parameters)
        #     request_url += f"?{query_string}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method=http_method.upper(),
                                           url=request_url,
                                           params=parameters if http_method.lower() == "get" else None,
                                           data=json.dumps(parameters) if http_method.lower() != "get" else None,
                                           # params=parameters if http_method.lower() == "get" else None,
                                           # data=json.dumps(parameters) if http_method.lower() != "get" else None,
                                           # data=json.dumps(parameters),
                                           headers=headers) as response:
                    text = await response.json()
                    if response.status == 200 and "application/json" in response.headers.get("Content-Type"):
                        return text

                    try:
                        error_message = json.loads(await response.text())["error_description"]
                        raise ValueError(error_message)
                    except:
                        raise ValueError(text)
            except Exception:
                raise
