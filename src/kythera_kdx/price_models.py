from typing import List, Dict, Any, Optional
import pandas as pd
from .authenticated_client import AuthenticatedClient
from .models_v1 import PriceModelDto, PriceModelInstrumentDto, PriceModelInstrumentGroupDto

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

    def get_price_model_instruments_raw(self, price_model_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        GET /v1/price-models/instruments
        Fetches price model instruments (raw JSON).
        """
        params = {}
        if price_model_id is not None:
            params["priceModelId"] = price_model_id
        response = self._client.get("/v1/price-models/instruments", params=params)
        return response.json()

    def get_price_model_instruments(self, price_model_id: Optional[int] = None) -> List[PriceModelInstrumentDto]:
        """
        GET /v1/price-models/instruments
        Fetches price model instruments (typed models).
        """
        data = self.get_price_model_instruments_raw(price_model_id)
        return [PriceModelInstrumentDto(**item) for item in data]

    def get_price_model_instruments_df(self, price_model_id: Optional[int] = None) -> pd.DataFrame:
        """
        GET /v1/price-models/instruments
        Fetches price model instruments (DataFrame).
        """
        data = self.get_price_model_instruments_raw(price_model_id)
        return pd.DataFrame(data)

    def get_price_model_instrument_groups_raw(self, price_model_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        GET /v1/price-models/instrument-groups
        Fetches price model instrument groups (raw JSON).
        """
        params = {}
        if price_model_id is not None:
            params["priceModelId"] = price_model_id
        response = self._client.get("/v1/price-models/instrument-groups", params=params)
        return response.json()

    def get_price_model_instrument_groups(self, price_model_id: Optional[int] = None) -> List[PriceModelInstrumentGroupDto]:
        """
        GET /v1/price-models/instrument-groups
        Fetches price model instrument groups (typed models).
        """
        data = self.get_price_model_instrument_groups_raw(price_model_id)
        return [PriceModelInstrumentGroupDto(**item) for item in data]

    def get_price_model_instrument_groups_df(self, price_model_id: Optional[int] = None) -> pd.DataFrame:
        """
        GET /v1/price-models/instrument-groups
        Fetches price model instrument groups (DataFrame).
        """
        data = self.get_price_model_instrument_groups_raw(price_model_id)
        return pd.DataFrame(data)
