"""
Example demonstrating MSAL authentication with the Kythera client.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from kythera_kdx.client import KytheraClient
from kythera_kdx.auth import MSALAuthenticator
from kythera_kdx.exceptions import KytheraAuthError


def example_api_key_auth():
    """Example using API key authentication."""
    print("=== API Key Authentication Example ===")
    
    # Initialize client with API key
    client = KytheraClient(
        base_url="https://api.kythera.com",
        api_key="your-api-key-here",
        timeout=30
    )
    
    print(f"Client initialized with API key authentication")
    print(f"Base URL: {client.base_url}")
    print(f"Using MSAL: {client.use_msal}")
    
    # Example usage (would make actual API calls)
    # response = client.get("/instruments")
    
    client.close()


def example_msal_auth():
    """Example using MSAL authentication."""
    print("\n=== MSAL Authentication Example ===")
    
    try:
        # Create MSAL authenticator
        authenticator = MSALAuthenticator(
            client_id="your-client-id",
            client_secret="your-client-secret",  # Optional for public clients
            tenant_id="your-tenant-id",
            scope="https://api.kythera.com/.default"
        )
        
        # Initialize client with MSAL
        client = KytheraClient(
            base_url="https://api.kythera.com",
            use_msal=True,
            msal_authenticator=authenticator,
            timeout=30
        )
        
        print(f"Client initialized with MSAL authentication")
        print(f"Base URL: {client.base_url}")
        print(f"Using MSAL: {client.use_msal}")
        
        # Example usage (would make actual API calls)
        # response = client.get("/instruments")
        
        client.close()
        
    except KytheraAuthError as e:
        print(f"Authentication error: {e}")


def example_msal_from_environment():
    """Example using MSAL authentication from environment variables."""
    print("\n=== MSAL from Environment Example ===")
    
    try:
        # Initialize client with MSAL from environment
        # Requires these environment variables:
        # - KYTHERA_CLIENT_ID
        # - KYTHERA_CLIENT_SECRET (optional)
        # - KYTHERA_TENANT_ID (optional)
        # - KYTHERA_SCOPE (optional)
        client = KytheraClient(
            base_url="https://api.kythera.com",
            use_msal=True,  # Will auto-create MSALAuthenticator from environment
            timeout=30
        )
        
        print(f"Client initialized with MSAL from environment")
        print(f"Base URL: {client.base_url}")
        print(f"Using MSAL: {client.use_msal}")
        
        client.close()
        
    except KytheraAuthError as e:
        print(f"Authentication error: {e}")


def example_context_manager():
    """Example using context manager."""
    print("\n=== Context Manager Example ===")
    
    # Use client as context manager
    with KytheraClient(api_key="your-api-key-here") as client:
        print(f"Client in context manager")
        # The session will be automatically closed when exiting the context
        
        # Example usage
        # response = client.get("/instruments")


if __name__ == "__main__":
    print("Kythera Client Examples with MSAL Authentication")
    print("=" * 50)
    
    example_api_key_auth()
    example_msal_auth()
    example_msal_from_environment()
    example_context_manager()
    
    print("\n=== Summary ===")
    print("The KytheraClient now supports:")
    print("1. API key authentication (legacy)")
    print("2. MSAL OAuth2 authentication")
    print("3. Automatic token refresh")
    print("4. Context manager support")
    print("5. Environment variable configuration")
