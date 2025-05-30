from typing import Any

from .authenticated_client import AuthenticatedClient


class InstrumentsClient:
    """Client for instrument-related endpoints."""
    
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_instruments(
        self,
        enabled_only: bool = True,
        fetch_characteristics: bool = True,
        fetch_group: bool = True,
    ) -> Any:
        """
        GET /v1/instruments
        Fetches all available instruments.
        """
        params = {
            "enabledOnly": enabled_only,
            "fetchCharacteristics": fetch_characteristics,
            "fetchGroup": fetch_group,
        }
        data = self._client.get("/v1/instruments", params=params)
        return data

    def create_instruments(self, instruments_data: Any) -> Any:
        """
        POST /v1/instruments
        Creates new instruments.
        """
        return self._client.post("/v1/instruments", data=instruments_data)
