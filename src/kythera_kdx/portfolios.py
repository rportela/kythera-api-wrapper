from typing import List, Dict, Any
from .authenticated_client import AuthenticatedClient
from .models_v1 import PortfolioDto
import pandas as pd

class PortfoliosClient:
    """Client for Portfolios endpoints."""
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_portfolios_raw(self) -> List[Dict[str, Any]]:
        """
        GET /v1/portfolios
        Fetches all available portfolios (raw JSON).
        """
        response = self._client.get("/v1/portfolios")
        return response.json()

    def get_portfolios(self) -> List[PortfolioDto]:
        """
        GET /v1/portfolios
        Fetches all available portfolios (typed models).
        """
        data = self.get_portfolios_raw()
        return [PortfolioDto(**item) for item in data]

    def get_portfolios_df(self) -> pd.DataFrame:
        """
        GET /v1/portfolios
        Fetches all available portfolios and returns a pandas DataFrame.
        """
        data = self.get_portfolios_raw()
        return pd.DataFrame(data)
