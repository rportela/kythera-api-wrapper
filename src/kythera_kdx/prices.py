from typing import List
from datetime import date

from .client import KytheraClient
from .models_v1 import PriceDto, OverrideInstrumentPriceRequest, PriceTypeDto


class PricesClient:
    def __init__(self, client: KytheraClient):
        self._client = client

    def get_all_prices(
        self,
        price_date: date,
        price_type_name: str,
    ) -> List[PriceDto]:
        """
        GET /v1/prices
        Fetches all prices for a given date and type.
        """
        params = {"priceDate": price_date.isoformat(), "priceTypeName": price_type_name}
        data = self._client.get("/v1/prices", params=params)
        return [PriceDto(**item) for item in data]

    def get_prices_by_instrument(
        self,
        instrument_id: int,
        price_date: date,
        price_type_name: str,
    ) -> List[PriceDto]:
        """
        GET /v1/prices/{instrumentId}
        Fetches prices for a given date, type and instrument.
        """
        params = {"priceDate": price_date.isoformat(), "priceTypeName": price_type_name}
        data = self._client.get(f"/v1/prices/{instrument_id}", params=params)
        return [PriceDto(**item) for item in data]

    def post_prices(
        self,
        requests: List[OverrideInstrumentPriceRequest],
    ) -> None:
        """
        POST /v1/prices
        Publishes instrument prices.
        """
        body = [req.dict() for req in requests]
        self._client.post("/v1/prices", data=body)

    def get_price_types(self) -> List[PriceTypeDto]:
        """
        GET /v1/prices/price-types
        Fetches all price types.
        """
        data = self._client.get("/v1/prices/price-types")
        return [PriceTypeDto(**item) for item in data]
