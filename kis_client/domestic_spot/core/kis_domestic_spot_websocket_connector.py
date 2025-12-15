import asyncio
from typing import Optional, Callable, Awaitable

import aiohttp

from kis_client.domestic_spot.constants.kis_spot_hosts import *
from kis_client.domestic_spot.enums.kis_domestic_spot_websocket_event_type import \
    KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType


class KoreaInvestmentSecuritiesDomesticSpotWebsocketConnector:
    async def open_and_subscribe_web_socket_stream_async(self,
                                                         query_string: str,
                                                         event_handler: Optional[Callable[
                                                             [KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType],
                                                             Awaitable[
                                                                 None]]] = None,
                                                         cancellation_event: Optional[asyncio.Event] = None):
        while cancellation_event is None or cancellation_event.is_set():
            try:
                request_url = f"{WEBSOCKET_HOST}{query_string}"
                async with aiohttp.ClientSession() as session:
                    websocket = await session.ws_connect(url=request_url)
                    await self._receive_message_async(websocket=websocket,
                                                      event_handler=event_handler,
                                                      cancellation_event=cancellation_event)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(str(e))

            await asyncio.sleep(0.5)

    async def _receive_message_async(self,
                                     websocket: aiohttp.ClientWebSocketResponse,
                                     event_handler: Optional[
                                         Callable[[KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType], Awaitable[
                                             None]]] = None,
                                     cancellation_event: Optional[asyncio.Event] = None):
        while not (cancellation_event and cancellation_event.is_set()):
            try:
                message = await websocket.receive()
            except Exception as e:
                print(str(e))
                break

            if message.type == (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.ERROR):
                break

    @staticmethod
    def _parse_event_type(message: str) -> KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType:
        if "markPriceUpdate" in message:
            return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.MarkPriceUpdate
        elif "kline" in message:
            return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.Kline
        elif "24hrTicker" in message:
            return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.Ticker
        elif "depthUpdate" in message:
            return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.DepthUpdate
        elif "ACCOUNT_UPDATE" in message:
            return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.AccountUpdate
        elif "ORDER_TRADE_UPDATE" in message:
            return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.OrderTradeUpdate
        elif "ACCOUNT_CONFIG_UPDATE" in message:
            return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.AccountConfigurationUpdate
        elif "STRATEGY_UPDATE" in message:
            return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.StrategyUpdate
        elif "GRID_UPDATE" in message:
            return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.GridUpdate
        elif "CONDITIONAL_ORDER_TRIGGER_REJECT" in message:
            return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.ConditionalOrderTriggerReject
        return KoreaInvestmentSecuritiesDomesticSpotWebsocketEventType.Unidentified
