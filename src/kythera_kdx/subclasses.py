from typing import List, Dict, Any, Optional
from datetime import date
import pandas as pd
from .authenticated_client import AuthenticatedClient
from .models_v1 import SubclassNavDto, SubclassDto

class SubclassesClient:
    """Client for Subclasses endpoints."""
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_subclass_navs_raw(
        self,
        date: Optional[date] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """
        GET /v1/subclasses/navs
        Fetches subclass NAVs for a given date or range (raw JSON).
        """
        params = {}
        if date:
            params["date"] = date.isoformat()
        if start_date:
            params["start-date"] = start_date.isoformat()
        if end_date:
            params["end-date"] = end_date.isoformat()
        response = self._client.get("/v1/subclasses/navs", params=params)
        return response.json()

    def get_subclass_navs(
        self,
        date: Optional[date] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[SubclassNavDto]:
        """
        GET /v1/subclasses/navs
        Fetches subclass NAVs for a given date or range (typed models).
        """
        data = self.get_subclass_navs_raw(date, start_date, end_date)
        return [SubclassNavDto(**item) for item in data]

    def get_subclass_navs_df(
        self,
        date: Optional[date] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> pd.DataFrame:
        """
        GET /v1/subclasses/navs
        Fetches subclass NAVs for a given date or range (DataFrame).
        """
        data = self.get_subclass_navs_raw(date, start_date, end_date)
        return pd.DataFrame(data)

    def get_subclasses_raw(self) -> List[Dict[str, Any]]:
        """
        GET /v1/subclasses
        Fetches all subclasses (raw JSON).
        """
        response = self._client.get("/v1/subclasses")
        return response.json()

    def get_subclasses(self) -> List[SubclassDto]:
        """
        GET /v1/subclasses
        Fetches all subclasses (typed models).
        """
        data = self.get_subclasses_raw()
        return [SubclassDto(**item) for item in data]

    def get_subclasses_df(self) -> pd.DataFrame:
        """
        GET /v1/subclasses
        Fetches all subclasses (DataFrame).
        """
        data = self.get_subclasses_raw()
        return pd.DataFrame(data)
