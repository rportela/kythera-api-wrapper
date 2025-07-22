from typing import List, Dict, Any, Optional

import pandas as pd

from .authenticated_client import AuthenticatedClient
from .models_v1 import IntradayPnlEntryDto, PnlExplainDto


class PnlClient:
    """Client for PnL (Profit and Loss) related endpoints."""
    
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_intraday_pnl_raw(self) -> List[Dict[str, Any]]:
        """
        GET /v1/pnl/intraday
        Fetches current intraday PnL and returns raw JSON data.
        """
        response = self._client.get("/v1/pnl/intraday")
        return response.json()

    def get_intraday_pnl(self) -> List[IntradayPnlEntryDto]:
        """
        GET /v1/pnl/intraday
        Fetches current intraday PnL and returns typed models.
        """
        data = self.get_intraday_pnl_raw()
        return [IntradayPnlEntryDto(**item) for item in data]

    def get_intraday_pnl_df(self) -> pd.DataFrame:
        """
        GET /v1/pnl/intraday
        Fetches current intraday PnL and returns a pandas DataFrame.
        """
        data = self.get_intraday_pnl_raw()
        return pd.DataFrame(data)

    def get_pnl_explain_raw(self, portfolio_id: Optional[int] = None, instrument_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        GET /v1/pnl/explain
        Fetches PnL explain data (raw JSON).
        """
        params = {}
        if portfolio_id is not None:
            params["portfolioId"] = portfolio_id
        if instrument_id is not None:
            params["instrumentId"] = instrument_id
        response = self._client.get("/v1/pnl/explain", params=params)
        return response.json()

    def get_pnl_explain(self, portfolio_id: Optional[int] = None, instrument_id: Optional[int] = None) -> List[PnlExplainDto]:
        """
        GET /v1/pnl/explain
        Fetches PnL explain data (typed models).
        """
        data = self.get_pnl_explain_raw(portfolio_id, instrument_id)
        return [PnlExplainDto(**item) for item in data]

    def get_pnl_explain_df(self, portfolio_id: Optional[int] = None, instrument_id: Optional[int] = None) -> pd.DataFrame:
        """
        GET /v1/pnl/explain
        Fetches PnL explain data (DataFrame).
        """
        data = self.get_pnl_explain_raw(portfolio_id, instrument_id)
        return pd.DataFrame(data)
