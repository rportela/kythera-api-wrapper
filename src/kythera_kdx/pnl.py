from typing import Any
from .authenticated_client import AuthenticatedClient


class PnlClient:
    """Client for PnL (Profit and Loss) related endpoints."""
    
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_intraday_pnl(self) -> Any:
        """
        GET /v1/pnl/intraday
        Fetches current intraday PnL.
        """
        data = self._client.get("/v1/pnl/intraday")
        return data
