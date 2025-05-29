from typing import List
from .client import KytheraClient
from .models_v1 import CalendarDto, CountryDto, CurrencyDto, InstitutionDto, InstitutionTypeDto, IssuerDto

class GlobalsClient:
    def __init__(self, client: KytheraClient):
        self._client = client

    def get_calendars(self) -> List[CalendarDto]:
        """
        GET /v1/globals/calendars
        Fetches all available calendars.
        """
        data = self._client.get("/v1/globals/calendars")
        return [CalendarDto(**item) for item in data]

    def get_countries(self) -> List[CountryDto]:
        """
        GET /v1/globals/countries
        Fetches all available countries.
        """
        data = self._client.get("/v1/globals/countries")
        return [CountryDto(**item) for item in data]

    def get_currencies(self) -> List[CurrencyDto]:
        """
        GET /v1/globals/currencies
        Fetches all available currencies.
        """
        data = self._client.get("/v1/globals/currencies")
        return [CurrencyDto(**item) for item in data]

    def get_institutions(
        self,
        fetch_characteristics: bool = False,
        fetch_nomenclatures: bool = False,
    ) -> List[InstitutionDto]:
        """
        GET /v1/globals/institutions
        Fetches all available institutions.
        """
        params = {
            "fetchCharacteristics": fetch_characteristics,
            "fetchNomenclatures": fetch_nomenclatures,
        }
        data = self._client.get("/v1/globals/institutions", params=params)
        return [InstitutionDto(**item) for item in data]

    def get_institution_types(self) -> List[InstitutionTypeDto]:
        """
        GET /v1/globals/institutions/types
        Fetches all available institution types.
        """
        data = self._client.get("/v1/globals/institutions/types")
        return [InstitutionTypeDto(**item) for item in data]

    def get_issuers(self, fetch_characteristics: bool = False) -> List[IssuerDto]:
        """
        GET /v1/globals/issuers
        Fetches all available issuers.
        """
        params = {"fetchCharacteristics": fetch_characteristics}
        data = self._client.get("/v1/globals/issuers", params=params)
        return [IssuerDto(**item) for item in data]
