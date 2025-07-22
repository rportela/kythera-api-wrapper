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

    def get_trade_fees_raw(self, trade_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        GET /v1/trades/fees
        Fetches trade fees (raw JSON).
        """
        params = {}
        if trade_id is not None:
            params["tradeId"] = trade_id
        response = self._client.get("/v1/trades/fees", params=params)
        return response.json()

    def get_trade_fees(self, trade_id: Optional[int] = None) -> List[TradeFeeDto]:
        """
        GET /v1/trades/fees
        Fetches trade fees (typed models).
        """
        data = self.get_trade_fees_raw(trade_id)
        return [TradeFeeDto(**item) for item in data]

    def get_trade_fees_df(self, trade_id: Optional[int] = None) -> pd.DataFrame:
        """
        GET /v1/trades/fees
        Fetches trade fees (DataFrame).
        """
        data = self.get_trade_fees_raw(trade_id)
        return pd.DataFrame(data)

    def get_trade_internals_raw(self, trade_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        GET /v1/trades/internals
        Fetches trade internals (raw JSON).
        """
        params = {}
        if trade_id is not None:
            params["tradeId"] = trade_id
        response = self._client.get("/v1/trades/internals", params=params)
        return response.json()

    def get_trade_internals(self, trade_id: Optional[int] = None) -> List[TradeInternalDto]:
        """
        GET /v1/trades/internals
        Fetches trade internals (typed models).
        """
        data = self.get_trade_internals_raw(trade_id)
        return [TradeInternalDto(**item) for item in data]

    def get_trade_internals_df(self, trade_id: Optional[int] = None) -> pd.DataFrame:
        """
        GET /v1/trades/internals
        Fetches trade internals (DataFrame).
        """
        data = self.get_trade_internals_raw(trade_id)
        return pd.DataFrame(data)
