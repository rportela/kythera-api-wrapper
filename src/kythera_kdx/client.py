"""
Enhanced client class for interacting with the Kythera API using httpx and MSAL authentication.
"""

import logging
from typing import Optional, Dict, Any, TypeVar
from urllib.parse import urljoin
import httpx
from pydantic import BaseModel

from .exceptions import (
    KytheraAPIError,
    KytheraAuthError,
    KytheraConnectionError,
    KytheraTimeoutError,
)
from .utils import format_endpoint, get_api_key_from_env

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class KytheraClient:
    """
    Client for interacting with the Kythera API.

    This class provides methods to authenticate and make requests to the Kythera API.
    """

    def __init__(
        self,
        base_url: str = "https://api.kythera.com",
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize the Kythera client.

        Args:
            base_url: The base URL for the Kythera API
            api_key: API key for authentication. If not provided, will try to get from KYTHERA_API_KEY environment variable
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or get_api_key_from_env()
        self.timeout = timeout
        self.session = httpx.Client(timeout=self.timeout)

        if self.api_key:
            self.session.headers.update(
                {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
            )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the Kythera API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request data for POST/PUT requests
            params: Query parameters

        Returns:
            API response as dictionary

        Raises:
            KytheraAPIError: When API returns an error
            KytheraAuthError: When authentication fails
            KytheraConnectionError: When connection fails
            KytheraTimeoutError: When request times out
        """
        url = urljoin(f"{self.base_url}/", format_endpoint(endpoint))

        try:
            response = self.session.request(
                method=method, url=url, json=data, params=params
            )

            if response.status_code == 401:
                raise KytheraAuthError(
                    "Authentication failed. Please check your API key."
                )

            if not response.is_success:
                try:
                    error_data = response.json()
                except ValueError:
                    error_data = {}

                raise KytheraAPIError(
                    f"API request failed with status {response.status_code}",
                    status_code=response.status_code,
                    response_data=error_data,
                )

            return response.json()

        except httpx.TimeoutException:
            raise KytheraTimeoutError(f"Request timed out after {self.timeout} seconds")
        except httpx.ConnectError as e:
            raise KytheraConnectionError(f"Failed to connect to Kythera API: {e}")
        except httpx.RequestError as e:
            raise KytheraAPIError(f"Request failed: {e}")

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a GET request to the API."""
        return self._make_request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a POST request to the API."""
        return self._make_request("POST", endpoint, data=data)

    def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a PUT request to the API."""
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request to the API."""
        return self._make_request("DELETE", endpoint)

    def set_api_key(self, api_key: str) -> None:
        """Set or update the API key."""
        self.api_key = api_key
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})
