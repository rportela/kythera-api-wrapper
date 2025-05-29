"""
Enhanced client class for interacting with the Kythera API using httpx and MSAL authentication.
"""

import logging
from typing import List, Optional, Dict, Any, TypeVar, Union, TYPE_CHECKING
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

if TYPE_CHECKING:
    from .auth import MSALAuthenticator

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class KytheraClient:
    """
    Client for interacting with the Kythera API.

    This class provides methods to authenticate and make requests to the Kythera API
    using either API key authentication or MSAL OAuth2 authentication.
    """

    def __init__(
        self,
        base_url: str = "https://api.kythera.com",
        api_key: Optional[str] = None,
        timeout: int = 30,
        use_msal: bool = False,
        msal_authenticator: Optional["MSALAuthenticator"] = None,
    ):
        """
        Initialize the Kythera client.

        Args:
            base_url: The base URL for the Kythera API
            api_key: API key for authentication. If not provided, will try to get from KYTHERA_API_KEY environment variable
            timeout: Request timeout in seconds
            use_msal: Whether to use MSAL authentication instead of API key
            msal_authenticator: Pre-configured MSAL authenticator instance
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.use_msal = use_msal
        self.msal_authenticator = msal_authenticator
        
        # Initialize HTTP client
        self.session = httpx.Client(timeout=self.timeout)
        
        # Set up authentication
        if use_msal:
            if not msal_authenticator:
                try:
                    # Dynamic import to avoid circular imports
                    from .auth import MSALAuthenticator
                    self.msal_authenticator = MSALAuthenticator.from_environment()
                except Exception as e:
                    raise KytheraAuthError(f"Failed to initialize MSAL authenticator: {e}")
            self._setup_msal_auth()
        else:
            self.api_key = api_key or get_api_key_from_env()
            if self.api_key:
                self._setup_api_key_auth()

    def _setup_api_key_auth(self) -> None:
        """Set up API key authentication headers."""
        if self.api_key:
            self.session.headers.update(
                {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
            )

    def _setup_msal_auth(self) -> None:
        """Set up MSAL authentication headers."""
        if self.msal_authenticator:
            try:
                access_token = self.msal_authenticator.get_access_token()
                self.session.headers.update(
                    {
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json",
                    }
                )
            except Exception as e:
                raise KytheraAuthError(f"Failed to get access token: {e}")

    def _refresh_auth_if_needed(self) -> None:
        """Refresh authentication token if using MSAL and token is expired."""
        if self.use_msal and self.msal_authenticator:
            try:
                access_token = self.msal_authenticator.get_access_token()
                self.session.headers.update({"Authorization": f"Bearer {access_token}"})
            except Exception as e:
                raise KytheraAuthError(f"Failed to refresh access token: {e}")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a request to the Kythera API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request data for POST/PUT requests
            params: Query parameters

        Returns:
            API response as dictionary or list of dictionaries

        Raises:
            KytheraAPIError: When API returns an error
            KytheraAuthError: When authentication fails
            KytheraConnectionError: When connection fails
            KytheraTimeoutError: When request times out
        """
        url = urljoin(f"{self.base_url}/", format_endpoint(endpoint))

        try:
            # Refresh authentication if needed
            self._refresh_auth_if_needed()
            
            response = self.session.request(
                method=method, url=url, json=data, params=params
            )

            if response.status_code == 401:
                # Try to refresh token once for MSAL
                if self.use_msal and self.msal_authenticator:
                    try:
                        access_token = self.msal_authenticator.get_access_token(force_refresh=True)
                        self.session.headers.update({"Authorization": f"Bearer {access_token}"})
                        
                        # Retry the request with new token
                        response = self.session.request(
                            method=method, url=url, json=data, params=params
                        )
                        
                        if response.status_code == 401:
                            raise KytheraAuthError("Authentication failed after token refresh")
                    except Exception as e:
                        raise KytheraAuthError(f"Authentication failed: {e}")
                else:
                    raise KytheraAuthError(
                        "Authentication failed. Please check your API key or MSAL configuration."
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
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make a GET request to the API."""
        return self._make_request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a POST request to the API."""
        response = self._make_request("POST", endpoint, data=data)
        if isinstance(response, list):
            # POST typically returns a single object, but handle list case
            return response[0] if response else {}
        return response

    def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a PUT request to the API."""
        response = self._make_request("PUT", endpoint, data=data)
        if isinstance(response, list):
            # PUT typically returns a single object, but handle list case
            return response[0] if response else {}
        return response

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request to the API."""
        response = self._make_request("DELETE", endpoint)
        if isinstance(response, list):
            # DELETE typically returns a single object, but handle list case
            return response[0] if response else {}
        return response

    def set_api_key(self, api_key: str) -> None:
        """Set or update the API key."""
        self.api_key = api_key
        self.use_msal = False
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def set_msal_authenticator(self, authenticator: "MSALAuthenticator") -> None:
        """Set or update the MSAL authenticator."""
        self.msal_authenticator = authenticator
        self.use_msal = True
        self._setup_msal_auth()

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()