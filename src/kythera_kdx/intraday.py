from typing import List
from .client import KytheraClient
from .models_v1 import IntradayPriceDto, IntradayRiskFactorValueDto


class IntradayClient:
    """Client for intraday data endpoints."""
    
    def __init__(self, client: KytheraClient):
        self._client = client

    def get_intraday_prices(self) -> List[IntradayPriceDto]:
        """
        GET /v1/intraday-prices
        Fetches all current instrument prices.
        """
        data = self._client.get("/v1/intraday-prices")
        return [IntradayPriceDto(**item) for item in data]

    def get_intraday_risk_factor_values(self) -> List[IntradayRiskFactorValueDto]:
        """
        GET /v1/intraday-risk-factor-values
        Fetches current risk factor values.
        """
        data = self._client.get("/v1/intraday-risk-factor-values")
        return [IntradayRiskFactorValueDto(**item) for item in data]
