from typing import List, Dict, Any
import pandas as pd

from .authenticated_client import AuthenticatedClient
from .models_v1 import IssuerDto


class IssuersClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_issuers_raw(self, fetch_characteristics: bool = False) -> List[Dict[str, Any]]:
        """
        GET /v1/issuers
        Fetches all available issuers and returns raw JSON data.
        """
        params = {"fetchCharacteristics": fetch_characteristics}
        response = self._client.get("/v1/issuers", params=params)
        return response.json()

    def get_issuers(self, fetch_characteristics: bool = False) -> List[IssuerDto]:
        """
        GET /v1/issuers
        Fetches all available issuers and returns typed models.
        """
        data = self.get_issuers_raw(fetch_characteristics)
        return [IssuerDto(**item) for item in data]

    def get_issuers_df(self, fetch_characteristics: bool = False) -> pd.DataFrame:
        """
        GET /v1/issuers
        Fetches all available issuers and returns a pandas DataFrame.
        """
        data = self.get_issuers_raw(fetch_characteristics)
        return pd.DataFrame(data)

    def get_issuer_parameters_raw(self) -> List[Dict[str, Any]]:
        """
        GET /v1/issuers/parameters
        Fetches all available issuer parameters and returns raw JSON data.
        """
        response = self._client.get("/v1/issuers/parameters")
        return response.json()

    def get_issuer_parameters(self) -> List[IssuerDto]:
        """
        GET /v1/issuers/parameters
        Fetches all available issuer parameters and returns typed models.
        """
        data = self.get_issuer_parameters_raw()
        return [IssuerDto(**item) for item in data]

    def get_issuer_parameters_df(self) -> pd.DataFrame:
        """
        GET /v1/issuers/parameters
        Fetches all available issuer parameters and returns a pandas DataFrame.
        """
        data = self.get_issuer_parameters_raw()
        return pd.DataFrame(data)
