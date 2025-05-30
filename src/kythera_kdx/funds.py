from datetime import date
from typing import List, Optional

from .authenticated_client import AuthenticatedClient
from .models_v1 import FundDto, FundNavDto

class FundsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_funds(
        self,
        enabled_only: Optional[bool] = True,
        fetch_characteristics: Optional[bool] = True,
    ) -> List[FundDto]:
        """
        GET /v1/funds
        Fetches all available funds.
        """
        params = {
            "enabledOnly": enabled_only,
            "fetchCharacteristics": fetch_characteristics,
        }
        data = self._client.get("/v1/funds", params=params)
        return [FundDto(**item) for item in data]

    def get_fund_navs(
        self,
        date: Optional[date] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        fund_id: Optional[int] = None,
    ) -> List[FundNavDto]:
        """
        GET /v1/funds/navs
        Fetches all available fund NAV entries for a given date or period.
        """
        params = {}
        if date:
            params["date"] = date.isoformat()
        if start_date:
            params["startDate"] = start_date.isoformat()
        if end_date:
            params["endDate"] = end_date.isoformat()
        if fund_id is not None:
            params["fundId"] = fund_id
        data = self._client.get("/v1/funds/navs", params=params)
        return [FundNavDto(**item) for item in data]
