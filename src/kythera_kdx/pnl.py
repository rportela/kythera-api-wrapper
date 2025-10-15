from typing import List, Dict, Any
from datetime import date

import pandas as pd

from .authenticated_client import AuthenticatedClient
from .models_v1 import IntradayPnlEntryDto


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

    def get_pnl_explain_raw(
        self,
        start_date: date,
        end_date: date,
        fund_family: str,
        discriminators: List[str]
    ) -> List[Dict[str, Any]]:
        """
        GET /v1/pnl/explain
        Retrieves PnL explain entries for the given range,
        fund family and discriminators (raw JSON).
        """
        params = {
            "start-date": start_date.isoformat(),
            "end-date": end_date.isoformat(),
            "fund-family": fund_family,
        }
        # Repeat the query param to send an array in query string
        for d in discriminators:
            params.setdefault("discriminator", [])
            params["discriminator"].append(d)
        response = self._client.get("/v1/pnl/explain", params=params)
        return response.json()

    def get_pnl_explain(
        self,
        start_date: date,
        end_date: date,
        fund_family: str,
        discriminators: List[str]
    ) -> List[Dict[str, Any]]:
        """
        GET /v1/pnl/explain
        Retrieves PnL explain entries for the given range,
        fund family and discriminators (typed models).
        """
        data = self.get_pnl_explain_raw(
            start_date, end_date, fund_family, discriminators
        )
        return data  # Return raw data since schema is not fully defined

    def get_pnl_explain_df(
        self,
        start_date: date,
        end_date: date,
        fund_family: str,
        discriminators: List[str]
    ) -> pd.DataFrame:
        """
        GET /v1/pnl/explain
        Retrieves PnL explain entries for the given range,
        fund family and discriminators (DataFrame).
        """
        data = self.get_pnl_explain_raw(
            start_date, end_date, fund_family, discriminators
        )
        return pd.DataFrame(data)
