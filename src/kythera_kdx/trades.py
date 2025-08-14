from datetime import date
from typing import List, Optional, Dict, Any

import pandas as pd

from .authenticated_client import AuthenticatedClient
from .models_v1 import TradeDto, TradeFeeDto, TradeInternalDto

class TradesClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_trades_raw(
        self,
        effective_date: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """
        GET /v1/trades
        Fetches all trades for a given effective date and returns raw JSON data.
        """
        params: dict = {}
        if effective_date:
            params["effectiveDate"] = effective_date.isoformat()
        response = self._client.get("/v1/trades", params=params)
        return response.json()

    def get_trades(
        self,
        effective_date: Optional[date] = None,
    ) -> List[TradeDto]:
        """
        GET /v1/trades
        Fetches all trades for a given effective date and returns typed models.
        """
        data = self.get_trades_raw(effective_date)
        return [TradeDto(**item) for item in data]

    def get_trades_df(
        self,
        effective_date: Optional[date] = None,
    ) -> pd.DataFrame:
        """
        GET /v1/trades
        Fetches all trades for a given effective date and returns a pandas DataFrame.
        """
        data = self.get_trades_raw(effective_date)
        return pd.DataFrame(data)

    def get_trade_fees_raw(self, effective_date: date) -> List[Dict[str, Any]]:
        """
        GET /v1/trades/fees
        Fetches trade fees for the provided effective date (raw JSON).
        """
        params = {"effective-date": effective_date.isoformat()}
        response = self._client.get("/v1/trades/fees", params=params)
        return response.json()

    def get_trade_fees(self, effective_date: date) -> List[TradeFeeDto]:
        """
        GET /v1/trades/fees
        Fetches trade fees for the provided effective date (typed models).
        """
        data = self.get_trade_fees_raw(effective_date)
        return [TradeFeeDto(**item) for item in data]

    def get_trade_fees_df(self, effective_date: date) -> pd.DataFrame:
        """
        GET /v1/trades/fees
        Fetches trade fees for the provided effective date (DataFrame).
        """
        data = self.get_trade_fees_raw(effective_date)
        return pd.DataFrame(data)

    def get_trade_internals_raw(self, effective_date: date) -> List[Dict[str, Any]]:
        """
        GET /v1/trades/internals
        Fetches internal trades for the provided effective date (raw JSON).
        """
        params = {"effective-date": effective_date.isoformat()}
        response = self._client.get("/v1/trades/internals", params=params)
        return response.json()

    def get_trade_internals(self, effective_date: date) -> List[TradeInternalDto]:
        """
        GET /v1/trades/internals
        Fetches internal trades for the provided effective date (typed models).
        """
        data = self.get_trade_internals_raw(effective_date)
        return [TradeInternalDto(**item) for item in data]

    def get_trade_internals_df(self, effective_date: date) -> pd.DataFrame:
        """
        GET /v1/trades/internals
        Fetches internal trades for the provided effective date (DataFrame).
        """
        data = self.get_trade_internals_raw(effective_date)
        return pd.DataFrame(data)
