from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import date
from .authenticated_client import AuthenticatedClient
from .models_v1 import IndexDto, IndexValueDto

class IndexesClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_indexes_raw(self, include_characteristics: bool = False) -> List[Dict[str, Any]]:
        """
        GET /v1/indexes
        Fetches all indexes (raw JSON).
        """
        params = {"include-characteristics": include_characteristics}
        response = self._client.get("/v1/indexes", params=params)
        return response.json()

    def get_indexes(self, include_characteristics: bool = False) -> List[IndexDto]:
        """
        GET /v1/indexes
        Fetches all indexes (typed models).
        """
        data = self.get_indexes_raw(include_characteristics)
        return [IndexDto(**item) for item in data]

    def get_indexes_df(self, include_characteristics: bool = False) -> pd.DataFrame:
        """
        GET /v1/indexes
        Fetches all indexes (DataFrame).
        """
        data = self.get_indexes_raw(include_characteristics)
        return pd.DataFrame(data)

    def get_index_values_raw(
        self,
        session_date: Optional[date] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """
        GET /v1/indexes/values
        Fetches index values by session-date or from-date/to-date (raw JSON).
        """
        params: Dict[str, Any] = {}
        if session_date:
            params["session-date"] = session_date.isoformat()
        if from_date:
            params["from-date"] = from_date.isoformat()
        if to_date:
            params["to-date"] = to_date.isoformat()
        response = self._client.get("/v1/indexes/values", params=params)
        return response.json()

    def get_index_values(
        self,
        session_date: Optional[date] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> List[IndexValueDto]:
        data = self.get_index_values_raw(session_date, from_date, to_date)
        return [IndexValueDto(**item) for item in data]

    def get_index_values_df(
        self,
        session_date: Optional[date] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> pd.DataFrame:
        data = self.get_index_values_raw(session_date, from_date, to_date)
        return pd.DataFrame(data)
