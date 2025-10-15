from typing import List, Dict, Any
import pandas as pd
from .authenticated_client import AuthenticatedClient
from .models_v1 import FundFamilyDto, FundFamilyRelationDto


class FundFamiliesClient:
    """Client for Fund Families endpoints."""

    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_fund_families_raw(self) -> List[Dict[str, Any]]:
        """
        GET /v1/fund-families
        Fetches all available fund families (raw JSON).
        """
        response = self._client.get("/v1/fund-families")
        return response.json()

    def get_fund_families(self) -> List[FundFamilyDto]:
        """
        GET /v1/fund-families
        Fetches all available fund families (typed models).
        """
        data = self.get_fund_families_raw()
        return [FundFamilyDto(**item) for item in data]

    def get_fund_families_df(self) -> pd.DataFrame:
        """
        GET /v1/fund-families
        Fetches all available fund families and returns a pandas DataFrame.
        """
        data = self.get_fund_families_raw()
        return pd.DataFrame(data)

    def get_fund_families_relations_raw(self) -> List[Dict[str, Any]]:
        """
        GET /v1/fund-families-relations
        Fetches all fund family <-> funds relations maps (raw JSON).
        """
        response = self._client.get("/v1/fund-families-relations")
        return response.json()

    def get_fund_families_relations(self) -> List[FundFamilyRelationDto]:
        """
        GET /v1/fund-families-relations
        Fetches all fund family <-> funds relations maps (typed models).
        """
        data = self.get_fund_families_relations_raw()
        return [FundFamilyRelationDto(**item) for item in data]

    def get_fund_families_relations_df(self) -> pd.DataFrame:
        """
        GET /v1/fund-families-relations
        Fetches all fund family <-> funds relations maps as DataFrame.
        """
        data = self.get_fund_families_relations_raw()
        return pd.DataFrame(data)