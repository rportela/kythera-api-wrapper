from datetime import date
from typing import List, Optional

from .authenticated_client import AuthenticatedClient
from .models_v1 import (
    RiskFactorDto,
    RiskFactorValueDto,
    OverrideRiskFactorValueRequest,
    RiskValueTypeDto,
)


class RiskFactorsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_risk_factors(self) -> List[RiskFactorDto]:
        """
        GET /v1/risk-factors
        Fetches all risk factors.
        """
        data = self._client.get("/v1/risk-factors")
        return [RiskFactorDto(**item) for item in data]

    def get_risk_factor_values(
        self,
        valuation_date: date,
    ) -> List[RiskFactorValueDto]:
        """
        GET /v1/risk-factor-values
        Fetches all risk factor values for a given date.
        """
        params = {"valuation-date": valuation_date.isoformat()}
        data = self._client.get("/v1/risk-factor-values", params=params)
        return [RiskFactorValueDto(**item) for item in data]

    def post_risk_factor_values(
        self,
        requests: List[OverrideRiskFactorValueRequest],
    ) -> None:
        """
        POST /v1/risk-factor-values
        Publishes risk factor values.
        """
        body = [req.dict() for req in requests]
        self._client.post("/v1/risk-factor-values", data=body)

    def get_risk_factor_value_types(self) -> List[RiskValueTypeDto]:
        """
        GET /v1/risk-factor-values/types
        Fetches all risk factor value types.
        """
        data = self._client.get("/v1/risk-factor-values/types")
        return [RiskValueTypeDto(**item) for item in data]
