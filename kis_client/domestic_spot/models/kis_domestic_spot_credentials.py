from typing import Optional

from pydantic import BaseModel


class KoreaInvestmentSecuritiesDomesticSpotCredentials(BaseModel):
    public_key: str
    private_key: str
    is_demo_account: bool = False
    is_corporate_account: bool = False
    public_rest_proxy_host: Optional[str] = None
    private_rest_proxy_host: Optional[str] = None
    public_websocket_proxy_host: Optional[str] = None
    private_websocket_proxy_host: Optional[str] = None
