from datetime import date
from typing import List, Optional

from .authenticated_client import AuthenticatedClient
from .models_v1 import TradeDto

class TradesClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_trades(
        self,
        effective_date: Optional[date] = None,
    ) -> List[TradeDto]:
        """
        GET /v1/trades
        Fetches all trades for a given effective date.
        """
        params: dict = {}
        if effective_date:
            params["effectiveDate"] = effective_date.isoformat()
        data = self._client.get("/v1/trades", params=params)
        return [TradeDto(**item) for item in data]
