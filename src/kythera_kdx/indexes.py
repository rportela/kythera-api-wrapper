from typing import List, Dict, Any
import pandas as pd
from .authenticated_client import AuthenticatedClient
from .models_v1 import IndexDto

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
