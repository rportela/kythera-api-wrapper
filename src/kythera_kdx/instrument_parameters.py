from typing import List

from .client import KytheraClient
from .models_v1 import InstrumentParameterDto

class InstrumentParametersClient:
    def __init__(self, client: KytheraClient):
        self._client = client

    def get_instrument_parameters(self) -> List[InstrumentParameterDto]:
        """
        GET /v1/instruments/parameters
        Fetches all available instrument parameters used in characteristics.
        """
        data = self._client.get("/v1/instruments/parameters")
        return [InstrumentParameterDto(**item) for item in data]
