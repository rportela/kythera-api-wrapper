from typing import List, Dict, Any, Optional

import pandas as pd

from .authenticated_client import AuthenticatedClient
from .models_v1 import InstrumentDto, InstrumentEventDto


class InstrumentsClient:
    """Client for instrument-related endpoints."""
    
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_instruments_raw(
        self,
        enabled_only: bool = True,
        fetch_characteristics: bool = True,
        fetch_baskets: bool = False,
        fetch_issuers: bool = False,
        fetch_cash_flows: bool = False,
        fetch_nomenclatures: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        GET /v1/instruments
        Fetches all available instruments and returns raw JSON data.
        """
        params = {
            "enabled-only": enabled_only,
            "fetch-characteristics": fetch_characteristics,
            "fetch-baskets": fetch_baskets,
            "fetch-issuers": fetch_issuers,
            "fetch-cash-flows": fetch_cash_flows,
            "fetch-nomenclatures": fetch_nomenclatures,
        }
        response = self._client.get("/v1/instruments", params=params)
        return response.json()

    def get_instruments(
        self,
        enabled_only: bool = True,
        fetch_characteristics: bool = True,
        fetch_baskets: bool = False,
        fetch_issuers: bool = False,
        fetch_cash_flows: bool = False,
        fetch_nomenclatures: bool = False,
    ) -> List[InstrumentDto]:
        """
        GET /v1/instruments
        Fetches all available instruments and returns typed models.
        """
        data = self.get_instruments_raw(
            enabled_only,
            fetch_characteristics,
            fetch_baskets,
            fetch_issuers,
            fetch_cash_flows,
            fetch_nomenclatures,
        )
        return [InstrumentDto(**item) for item in data]

    def get_instruments_df(
        self,
        enabled_only: bool = True,
        fetch_characteristics: bool = True,
        fetch_baskets: bool = False,
        fetch_issuers: bool = False,
        fetch_cash_flows: bool = False,
        fetch_nomenclatures: bool = False,
    ) -> pd.DataFrame:
        """
        GET /v1/instruments
        Fetches all available instruments and returns a pandas DataFrame.
        """
        data = self.get_instruments_raw(
            enabled_only,
            fetch_characteristics,
            fetch_baskets,
            fetch_issuers,
            fetch_cash_flows,
            fetch_nomenclatures,
        )
        return pd.DataFrame(data)

    def create_instruments(self, instruments_data: List[Dict[str, Any]]) -> None:
        """
        POST /v1/instruments
        Creates new instruments.
        """
        body = instruments_data
        response = self._client.post("/v1/instruments", data=body)  # type: ignore
        response.raise_for_status()

    def get_instrument_events_raw(self, instrument_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        GET /v1/instruments/events
        Fetches instrument events (raw JSON).
        """
        params = {}
        if instrument_id is not None:
            params["instrumentId"] = instrument_id
        response = self._client.get("/v1/instruments/events", params=params)
        return response.json()

    def get_instrument_events(self, instrument_id: Optional[int] = None) -> List[InstrumentEventDto]:
        """
        GET /v1/instruments/events
        Fetches instrument events (typed models).
        """
        data = self.get_instrument_events_raw(instrument_id)
        return [InstrumentEventDto(**item) for item in data]

    def get_instrument_events_df(self, instrument_id: Optional[int] = None) -> pd.DataFrame:
        """
        GET /v1/instruments/events
        Fetches instrument events (DataFrame).
        """
        data = self.get_instrument_events_raw(instrument_id)
        return pd.DataFrame(data)
