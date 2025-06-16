from datetime import date
from typing import List, Optional, Dict, Any

import pandas as pd

from .authenticated_client import AuthenticatedClient
from .models_v1 import FundDto, FundNavDto, FundCounterpartyMarginDto, FundRiskMeasureDto, FundFamilyDto, FundFamilyRelationDto

class FundsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_funds_raw(
        self,
        enabled_only: Optional[bool] = True,
        fetch_characteristics: Optional[bool] = True,
    ) -> List[Dict[str, Any]]:
        """
        GET /v1/funds
        Fetches all available funds and returns raw JSON data.
        """
        params = {
            "enabledOnly": enabled_only,
            "fetchCharacteristics": fetch_characteristics,
        }
        response = self._client.get("/v1/funds", params=params)
        return response.json()

    def get_funds(
        self,
        enabled_only: Optional[bool] = True,
        fetch_characteristics: Optional[bool] = True,
    ) -> List[FundDto]:
        """
        GET /v1/funds
        Fetches all available funds and returns typed models.
        """
        data = self.get_funds_raw(enabled_only, fetch_characteristics)
        return [FundDto(**item) for item in data]

    def get_funds_df(
        self,
        enabled_only: Optional[bool] = True,
        fetch_characteristics: Optional[bool] = True,
    ) -> pd.DataFrame:
        """
        GET /v1/funds
        Fetches all available funds and returns a pandas DataFrame.
        """
        data = self.get_funds_raw(enabled_only, fetch_characteristics)
        return pd.DataFrame(data)

    def get_fund_navs_raw(
        self,
        date: Optional[date] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        fund_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        GET /v1/funds/navs
        Fetches all available fund NAV entries for a given date or period and returns raw JSON data.
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
        response = self._client.get("/v1/funds/navs", params=params)
        return response.json()

    def get_fund_navs(
        self,
        date: Optional[date] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        fund_id: Optional[int] = None,
    ) -> List[FundNavDto]:
        """
        GET /v1/funds/navs
        Fetches all available fund NAV entries for a given date or period and returns typed models.
        """
        data = self.get_fund_navs_raw(date, start_date, end_date, fund_id)
        return [FundNavDto(**item) for item in data]

    def get_fund_navs_df(
        self,
        date: Optional[date] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        fund_id: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        GET /v1/funds/navs
        Fetches all available fund NAV entries for a given date or period and returns a pandas DataFrame.
        """
        data = self.get_fund_navs_raw(date, start_date, end_date, fund_id)
        return pd.DataFrame(data)

    def get_fund_counterparty_margins_raw(self, session_date: date) -> List[Dict[str, Any]]:
        """
        GET /v1/fund-counterparty-margins
        Fetches all fund counterparty margins for a specified session date (raw JSON).
        """
        params = {"session-date": session_date.isoformat()}
        response = self._client.get("/v1/fund-counterparty-margins", params=params)
        return response.json()

    def get_fund_counterparty_margins(self, session_date: date) -> List[FundCounterpartyMarginDto]:
        """
        GET /v1/fund-counterparty-margins
        Fetches all fund counterparty margins for a specified session date (typed models).
        """
        data = self.get_fund_counterparty_margins_raw(session_date)
        return [FundCounterpartyMarginDto(**item) for item in data]

    def get_fund_counterparty_margins_df(self, session_date: date) -> pd.DataFrame:
        """
        GET /v1/fund-counterparty-margins
        Fetches all fund counterparty margins for a specified session date (DataFrame).
        """
        data = self.get_fund_counterparty_margins_raw(session_date)
        return pd.DataFrame(data)

    def get_fund_risk_measures_raw(self, effective_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """
        GET /v1/fund-risk-measures
        Fetches all available risk measures for funds on a specified effective date (raw JSON).
        """
        params = {}
        if effective_date:
            params["effective-date"] = effective_date.isoformat()
        response = self._client.get("/v1/fund-risk-measures", params=params)
        return response.json()

    def get_fund_risk_measures(self, effective_date: Optional[date] = None) -> List[FundRiskMeasureDto]:
        """
        GET /v1/fund-risk-measures
        Fetches all available risk measures for funds on a specified effective date (typed models).
        """
        data = self.get_fund_risk_measures_raw(effective_date)
        return [FundRiskMeasureDto(**item) for item in data]

    def get_fund_risk_measures_df(self, effective_date: Optional[date] = None) -> pd.DataFrame:
        """
        GET /v1/fund-risk-measures
        Fetches all available risk measures for funds on a specified effective date (DataFrame).
        """
        data = self.get_fund_risk_measures_raw(effective_date)
        return pd.DataFrame(data)

    def get_fund_families_raw(self) -> List[Dict[str, Any]]:
        """
        GET /v1/fund-families
        Fetches all fund families (raw JSON).
        """
        response = self._client.get("/v1/fund-families")
        return response.json()

    def get_fund_families(self) -> List[FundFamilyDto]:
        """
        GET /v1/fund-families
        Fetches all fund families (typed models).
        """
        data = self.get_fund_families_raw()
        return [FundFamilyDto(**item) for item in data]

    def get_fund_families_df(self) -> pd.DataFrame:
        """
        GET /v1/fund-families
        Fetches all fund families (DataFrame).
        """
        data = self.get_fund_families_raw()
        return pd.DataFrame(data)

    def get_fund_family_relations_raw(self) -> List[Dict[str, Any]]:
        """
        GET /v1/fund-families/relations
        Fetches all fund family <-> funds relations maps (raw JSON).
        """
        response = self._client.get("/v1/fund-families-relations")
        return response.json()

    def get_fund_family_relations(self) -> List[FundFamilyRelationDto]:
        """
        GET /v1/fund-families/relations
        Fetches all fund family <-> funds relations maps (typed models).
        """
        data = self.get_fund_family_relations_raw()
        return [FundFamilyRelationDto(**item) for item in data]

    def get_fund_family_relations_df(self) -> pd.DataFrame:
        """
        GET /v1/fund-families/relations
        Fetches all fund family <-> funds relations maps (DataFrame).
        """
        data = self.get_fund_family_relations_raw()
        return pd.DataFrame(data)
