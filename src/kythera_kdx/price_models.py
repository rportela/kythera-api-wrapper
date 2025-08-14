from typing import List, Dict, Any
import pandas as pd
from .authenticated_client import AuthenticatedClient
from .models_v1 import PriceModelDto, InstrumentPriceModelDto, InstrumentGroupPriceModelDto

class PriceModelsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_price_models_raw(self) -> List[Dict[str, Any]]:
        """
        GET /v1/price-models
        Fetches all price models (raw JSON).
        """
        response = self._client.get("/v1/price-models")
        return response.json()

    def get_price_models(self) -> List[PriceModelDto]:
        """
        GET /v1/price-models
        Fetches all price models (typed models).
        """
        data = self.get_price_models_raw()
        return [PriceModelDto(**item) for item in data]

    def get_price_models_df(self) -> pd.DataFrame:
        """
        GET /v1/price-models
        Fetches all price models (DataFrame).
        """
        data = self.get_price_models_raw()
        return pd.DataFrame(data)

    def get_price_model_instruments_raw(self, include_action_risk_factors: bool = False) -> List[Dict[str, Any]]:
        """
        GET /v1/price-models/instruments
        Fetches instrument price models (raw JSON).
        """
        params = {"include-action-risk-factors": include_action_risk_factors}
        response = self._client.get("/v1/price-models/instruments", params=params)
        return response.json()

    def get_price_model_instruments(self, include_action_risk_factors: bool = False) -> List[InstrumentPriceModelDto]:
        """
        GET /v1/price-models/instruments
        Fetches instrument price models (typed models).
        """
        data = self.get_price_model_instruments_raw(include_action_risk_factors)
        return [InstrumentPriceModelDto(**item) for item in data]

    def get_price_model_instruments_df(self, include_action_risk_factors: bool = False) -> pd.DataFrame:
        """
        GET /v1/price-models/instruments
        Fetches instrument price models (DataFrame).
        """
        data = self.get_price_model_instruments_raw(include_action_risk_factors)
        return pd.DataFrame(data)

    def get_price_model_instrument_groups_raw(self, include_action_risk_factors: bool = False) -> List[Dict[str, Any]]:
        """
        GET /v1/price-models/instrument-groups
        Fetches instrument group price models (raw JSON).
        """
        params = {"include-action-risk-factors": include_action_risk_factors}
        response = self._client.get("/v1/price-models/instrument-groups", params=params)
        return response.json()

    def get_price_model_instrument_groups(self, include_action_risk_factors: bool = False) -> List[InstrumentGroupPriceModelDto]:
        """
        GET /v1/price-models/instrument-groups
        Fetches instrument group price models (typed models).
        """
        data = self.get_price_model_instrument_groups_raw(include_action_risk_factors)
        return [InstrumentGroupPriceModelDto(**item) for item in data]

    def get_price_model_instrument_groups_df(self, include_action_risk_factors: bool = False) -> pd.DataFrame:
        """
        GET /v1/price-models/instrument-groups
        Fetches instrument group price models (DataFrame).
        """
        data = self.get_price_model_instrument_groups_raw(include_action_risk_factors)
        return pd.DataFrame(data)
