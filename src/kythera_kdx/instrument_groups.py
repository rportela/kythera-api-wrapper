from typing import List
from .client import KytheraClient
from .models_v1 import InstrumentGroupDto

class InstrumentGroupsClient:
    def __init__(self, client: KytheraClient):
        self._client = client

    def get_instrument_groups(
        self,
        fetch_characteristics: bool = True,
        fetch_nomenclatures: bool = True,
    ) -> List[InstrumentGroupDto]:
        """
        GET /v1/instrument-groups
        Fetches all available instrument groups.
        """
        params = {
            "fetchCharacteristics": fetch_characteristics,
            "fetchNomenclatures": fetch_nomenclatures,
        }
        data = self._client.get("/v1/instrument-groups", params=params)
        return [InstrumentGroupDto(**item) for item in data]
