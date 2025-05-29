"""
Authentication module for Kythera API using Microsoft MSAL.
"""

import os
from typing import Optional, Dict, Any
from msal import ConfidentialClientApplication, PublicClientApplication
import logging

from .exceptions import KytheraAuthError

logger = logging.getLogger(__name__)


class MSALAuthenticator:
    """
    Microsoft MSAL-based authenticator for Kythera API.
    
    This class handles OAuth 2.0 authentication using Microsoft Authentication Library (MSAL).
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: Optional[str] = None,
        authority: Optional[str] = None,
        scope: Optional[str] = None,
        tenant_id: Optional[str] = None
    ):
        """
        Initialize the MSAL authenticator.
        
        Args:
            client_id: The application (client) ID
            client_secret: The client secret (for confidential client apps)
            authority: The authority URL (e.g., https://login.microsoftonline.com/{tenant})
            scope: The scope for the token request
            tenant_id: The tenant ID (if not included in authority)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope or "https://graph.microsoft.com/.default"
        
        # Build authority URL
        if authority:
            self.authority = authority
        elif tenant_id:
            self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        else:
            self.authority = "https://login.microsoftonline.com/common"
        
        # Initialize the appropriate MSAL client
        if client_secret:
            self.app = ConfidentialClientApplication(
                client_id=self.client_id,
                client_credential=self.client_secret,
                authority=self.authority
            )
        else:
            self.app = PublicClientApplication(
                client_id=self.client_id,
                authority=self.authority
            )
        
        self._access_token: Optional[str] = None
        self._token_info: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_environment(cls) -> "MSALAuthenticator":
        """
        Create authenticator from environment variables.
        
        Expected environment variables:
        - KYTHERA_CLIENT_ID
        - KYTHERA_CLIENT_SECRET (optional, for confidential clients)
        - KYTHERA_TENANT_ID (optional)
        - KYTHERA_AUTHORITY (optional, overrides tenant_id)
        - KYTHERA_SCOPE (optional)
        """
        client_id = os.getenv("KYTHERA_CLIENT_ID")
        if not client_id:
            raise KytheraAuthError("KYTHERA_CLIENT_ID environment variable is required")
        
        return cls(
            client_id=client_id,
            client_secret=os.getenv("KYTHERA_CLIENT_SECRET"),
            authority=os.getenv("KYTHERA_AUTHORITY"),
            scope=os.getenv("KYTHERA_SCOPE"),
            tenant_id=os.getenv("KYTHERA_TENANT_ID")
        )
    
    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Get a valid access token.
        
        Args:
            force_refresh: Force refresh the token even if current one is valid
            
        Returns:
            Valid access token
            
        Raises:
            KytheraAuthError: If authentication fails
        """
        if not force_refresh and self._access_token and self._is_token_valid():
            return self._access_token
        
        return self._acquire_token()
    
    def _acquire_token(self) -> str:
        """Acquire a new access token."""
        try:
            # Try to get token silently first (from cache)
            accounts = self.app.get_accounts()
            if accounts:
                result = self.app.acquire_token_silent(
                    scopes=[self.scope],
                    account=accounts[0]
                )
                if result and "access_token" in result:
                    self._store_token(result)
                    return self._access_token
            
            # If silent acquisition fails, try different flows based on client type
            if isinstance(self.app, ConfidentialClientApplication):
                # Client credentials flow for service-to-service authentication
                result = self.app.acquire_token_for_client(scopes=[self.scope])
            else:
                # Device code flow for public clients
                result = self._acquire_token_device_flow()
            
            if "access_token" not in result:
                error_msg = result.get("error_description", "Unknown authentication error")
                raise KytheraAuthError(f"Authentication failed: {error_msg}")
            
            self._store_token(result)
            return self._access_token
            
        except Exception as e:
            if isinstance(e, KytheraAuthError):
                raise
            raise KytheraAuthError(f"Token acquisition failed: {str(e)}")
    
    def _acquire_token_device_flow(self) -> Dict[str, Any]:
        """Acquire token using device code flow."""
        flow = self.app.initiate_device_flow(scopes=[self.scope])
        
        if "user_code" not in flow:
            raise KytheraAuthError("Failed to create device flow")
        
        print(flow["message"])
        
        # Wait for the user to complete the flow
        result = self.app.acquire_token_by_device_flow(flow)
        return result
    
    def _store_token(self, token_response: Dict[str, Any]) -> None:
        """Store token information."""
        self._token_info = token_response
        self._access_token = token_response["access_token"]
        logger.info("Access token acquired successfully")
    
    def _is_token_valid(self) -> bool:
        """Check if the current token is still valid."""
        if not self._token_info:
            return False
        
        # Add some buffer time (5 minutes) before expiration
        import time
        expires_in = self._token_info.get("expires_in", 0)
        token_acquired_time = getattr(self, "_token_acquired_time", 0)
        buffer_time = 300  # 5 minutes
        
        return time.time() < (token_acquired_time + expires_in - buffer_time)
    
    def clear_cache(self) -> None:
        """Clear the token cache."""
        accounts = self.app.get_accounts()
        for account in accounts:
            self.app.remove_account(account)
        
        self._access_token = None
        self._token_info = None
        logger.info("Token cache cleared")
