from typing import Any
from .client import KytheraClient


class PnlClient:
    """Client for PnL (Profit and Loss) related endpoints."""
    
    def __init__(self, client: KytheraClient):
        self._client = client

    def get_intraday_pnl(self) -> Any:
        """
        GET /v1/pnl/intraday
        Fetches current intraday PnL.
        """
        data = self._client.get("/v1/pnl/intraday")
        return data
