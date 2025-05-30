from datetime import date
from typing import List, Optional

from .authenticated_client import AuthenticatedClient
from .models_v1 import PositionDto

class PositionsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_positions(
        self,
        position_date: Optional[date] = None,
        is_open: bool = True,
    ) -> List[PositionDto]:
        """
        GET /v1/positions
        Fetches all position entries for a given date.
        """
        params: dict = {}
        if position_date:
            params["positionDate"] = position_date.isoformat()
        params["isOpen"] = is_open
        data = self._client.get("/v1/positions", params=params)
        return [PositionDto(**item) for item in data]
