from typing import Optional
from .client import KytheraClient

class AddInClient:
    def __init__(self, client: KytheraClient):
        self._client = client

    def get_add_in(self) -> dict:
        """
        GET /add-in
        Fetches add-in information.
        """
        return self._client.get("/add-in")

    def get_add_in_core(self, version: str) -> dict:
        """
        GET /add-in/core?version={version}
        Fetches core add-in information for a specific version.
        """
        params = {"version": version}
        return self._client.get("/add-in/core", params=params)

    def get_add_in_version(self) -> dict:
        """
        GET /add-in/version
        Fetches current add-in version.
        """
        return self._client.get("/add-in/version")
