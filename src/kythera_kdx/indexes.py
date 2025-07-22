from typing import List, Dict, Any, Optional
import pandas as pd
from .authenticated_client import AuthenticatedClient
from .models_v1 import IndexDto

class IndexesClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_indexes_raw(self, date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        GET /v1/indexes
        Fetches all indexes (raw JSON).
        """
        params = {}
        if date:
            params["date"] = date
        response = self._client.get("/v1/indexes", params=params)
        return response.json()

    def get_indexes(self, date: Optional[str] = None) -> List[IndexDto]:
        """
        GET /v1/indexes
        Fetches all indexes (typed models).
        """
        data = self.get_indexes_raw(date)
        return [IndexDto(**item) for item in data]

    def get_indexes_df(self, date: Optional[str] = None) -> pd.DataFrame:
        """
        GET /v1/indexes
        Fetches all indexes (DataFrame).
        """
        data = self.get_indexes_raw(date)
        return pd.DataFrame(data)
