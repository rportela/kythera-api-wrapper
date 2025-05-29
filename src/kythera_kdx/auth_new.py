"""
MSAL (Microsoft Authentication Library) authenticator for Kythera API.

This module provides MSAL-based authentication for the Kythera API client,
supporting both confidential and public client applications with automatic
token management and refresh capabilities.
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List, Union
from msal import ConfidentialClientApplication, PublicClientApplication

from .exceptions import KytheraAuthError

logger = logging.getLogger(__name__)


class MSALAuthenticator:
    """
    MSAL authenticator for Kythera API.
    
    Supports both ConfidentialClientApplication (for server-to-server scenarios)
    and PublicClientApplication (for interactive scenarios) with automatic
    token caching and refresh.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: Optional[str] = None,
        authority: str = "https://login.microsoftonline.com/common",
        scopes: Optional[List[str]] = None,
        tenant_id: Optional[str] = None,
    ):
        """
        Initialize the MSAL authenticator.

        Args:
            client_id: Azure AD application client ID
            client_secret: Azure AD application client secret (for confidential clients)
            authority: Azure AD authority URL
            scopes: List of scopes to request
            tenant_id: Azure AD tenant ID (optional, can be included in authority)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes or ["https://api.kythera.com/.default"]
        
        # Build authority URL with tenant if provided
        if tenant_id and tenant_id not in authority:
            self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        else:
            self.authority = authority
        
        # Token cache
        self._cached_token: Optional[str] = None
        self._token_expires_at: Optional[float] = None
        self._app: Optional[Union[ConfidentialClientApplication, PublicClientApplication]] = None
        
        # Initialize MSAL application
        self._initialize_app()

    def _initialize_app(self) -> None:
        """Initialize the MSAL application (confidential or public client)."""
        try:
            if self.client_secret:
                # Confidential client application (server-to-server)
                self._app = ConfidentialClientApplication(
                    client_id=self.client_id,
                    client_credential=self.client_secret,
                    authority=self.authority,
                )
                logger.info("Initialized MSAL ConfidentialClientApplication")
            else:
                # Public client application (interactive)
                self._app = PublicClientApplication(
                    client_id=self.client_id,
                    authority=self.authority,
                )
                logger.info("Initialized MSAL PublicClientApplication")
        except Exception as e:
            raise KytheraAuthError(f"Failed to initialize MSAL application: {e}")

    @classmethod
    def from_environment(cls) -> "MSALAuthenticator":
        """
        Create an authenticator from environment variables.
        
        Expected environment variables:
        - AZURE_CLIENT_ID: Azure AD application client ID
        - AZURE_CLIENT_SECRET: Azure AD application client secret (optional)
        - AZURE_TENANT_ID: Azure AD tenant ID (optional)
        - AZURE_AUTHORITY: Azure AD authority URL (optional)
        - KYTHERA_SCOPES: Comma-separated list of scopes (optional)
        
        Returns:
            MSALAuthenticator instance configured from environment
            
        Raises:
            KytheraAuthError: If required environment variables are missing
        """
        client_id = os.getenv("AZURE_CLIENT_ID")
        if not client_id:
            raise KytheraAuthError("AZURE_CLIENT_ID environment variable is required")
        
        client_secret = os.getenv("AZURE_CLIENT_SECRET")
        tenant_id = os.getenv("AZURE_TENANT_ID")
        authority = os.getenv("AZURE_AUTHORITY", "https://login.microsoftonline.com/common")
        
        scopes_str = os.getenv("KYTHERA_SCOPES")
        scopes = [s.strip() for s in scopes_str.split(",")] if scopes_str else None
        
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            authority=authority,
            scopes=scopes,
            tenant_id=tenant_id,
        )

    def _is_token_expired(self) -> bool:
        """Check if the current token is expired or will expire soon."""
        if not self._token_expires_at:
            return True
        
        # Add 5 minute buffer before expiration
        buffer_seconds = 300
        return time.time() >= (self._token_expires_at - buffer_seconds)

    def _acquire_token_for_confidential_client(self, force_refresh: bool = False) -> str:
        """Acquire token using client credentials flow (confidential client)."""
        if not force_refresh and not self._is_token_expired() and self._cached_token:
            return self._cached_token
        
        if not self._app:
            raise KytheraAuthError("MSAL application not initialized")
        
        if not isinstance(self._app, ConfidentialClientApplication):
            raise KytheraAuthError("Expected ConfidentialClientApplication for confidential client flow")
        
        try:
            result = self._app.acquire_token_for_client(scopes=self.scopes)
            
            if "access_token" in result:
                self._cached_token = result["access_token"]
                # MSAL returns expires_in (seconds from now)
                expires_in = result.get("expires_in", 3600)
                if isinstance(expires_in, (int, float)):
                    self._token_expires_at = time.time() + expires_in
                else:
                    self._token_expires_at = time.time() + 3600  # Default 1 hour
                logger.info("Successfully acquired access token using client credentials")
                return self._cached_token
            else:
                error_msg = result.get("error_description", result.get("error", "Unknown error"))
                raise KytheraAuthError(f"Failed to acquire token: {error_msg}")
                
        except Exception as e:
            raise KytheraAuthError(f"Token acquisition failed: {e}")

    def _acquire_token_for_public_client(self, force_refresh: bool = False) -> str:
        """Acquire token using device code flow (public client)."""
        if not force_refresh and not self._is_token_expired() and self._cached_token:
            return self._cached_token
        
        if not self._app:
            raise KytheraAuthError("MSAL application not initialized")
        
        if not isinstance(self._app, PublicClientApplication):
            raise KytheraAuthError("Expected PublicClientApplication for public client flow")
        
        try:
            # Try to get token silently first
            accounts = self._app.get_accounts()
            if accounts and not force_refresh:
                result = self._app.acquire_token_silent(scopes=self.scopes, account=accounts[0])
                if result and "access_token" in result:
                    self._cached_token = result["access_token"]
                    expires_in = result.get("expires_in", 3600)
                    if isinstance(expires_in, (int, float)):
                        self._token_expires_at = time.time() + expires_in
                    else:
                        self._token_expires_at = time.time() + 3600  # Default 1 hour
                    logger.info("Successfully acquired access token silently")
                    return self._cached_token
            
            # If silent acquisition fails, use device code flow
            flow = self._app.initiate_device_flow(scopes=self.scopes)
            if "user_code" not in flow:
                raise KytheraAuthError("Failed to create device flow")
            
            print(flow["message"])  # This contains the device code instructions
            
            result = self._app.acquire_token_by_device_flow(flow)
            
            if "access_token" in result:
                self._cached_token = result["access_token"]
                expires_in = result.get("expires_in", 3600)
                if isinstance(expires_in, (int, float)):
                    self._token_expires_at = time.time() + expires_in
                else:
                    self._token_expires_at = time.time() + 3600  # Default 1 hour
                logger.info("Successfully acquired access token using device code flow")
                return self._cached_token
            else:
                error_msg = result.get("error_description", result.get("error", "Unknown error"))
                raise KytheraAuthError(f"Failed to acquire token: {error_msg}")
                
        except Exception as e:
            raise KytheraAuthError(f"Token acquisition failed: {e}")

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Get a valid access token.
        
        Args:
            force_refresh: Force token refresh even if current token is valid
            
        Returns:
            Valid access token
            
        Raises:
            KytheraAuthError: If token acquisition fails
        """
        if not self._app:
            raise KytheraAuthError("MSAL application not initialized")
        
        if self.client_secret:
            # Confidential client - use client credentials flow
            return self._acquire_token_for_confidential_client(force_refresh)
        else:
            # Public client - use device code flow
            return self._acquire_token_for_public_client(force_refresh)

    def clear_cache(self) -> None:
        """Clear the token cache."""
        self._cached_token = None
        self._token_expires_at = None
        logger.info("Token cache cleared")

    def is_authenticated(self) -> bool:
        """Check if we have a valid, non-expired token."""
        return bool(self._cached_token and not self._is_token_expired())

    def get_token_info(self) -> Dict[str, Any]:
        """
        Get information about the current token.
        
        Returns:
            Dictionary with token information
        """
        return {
            "has_token": bool(self._cached_token),
            "is_expired": self._is_token_expired(),
            "expires_at": self._token_expires_at,
            "time_to_expiry": (
                self._token_expires_at - time.time() 
                if self._token_expires_at else None
            ),
        }
