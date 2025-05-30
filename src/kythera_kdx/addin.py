from .authenticated_client import AuthenticatedClient


class AddInClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_add_in(self) -> dict:
        """
        GET /add-in
        Fetches add-in information.
        """
        return self._client.get("/add-in").json()

    def get_add_in_core(self, version: str) -> dict:
        """
        GET /add-in/core?version={version}
        Fetches core add-in information for a specific version.
        """
        params = {"version": version}
        return self._client.get("/add-in/core", params=params).json()

    def get_add_in_version(self) -> str:
        """
        GET /add-in/version
        Fetches current add-in version.
        """
        return self._client.get("/add-in/version").text
