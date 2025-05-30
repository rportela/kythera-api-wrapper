"""
Example demonstrating the new AuthenticatedClient usage.

This example shows how to use the unified AuthenticatedClient that combines
authentication and API request capabilities.
"""

import os
from kythera_kdx import AuthenticatedClient


def example_service_principal_auth():
    """Example using service principal authentication (with client_secret)."""
    print("=== Service Principal Authentication Example ===")
    
    # Create client with service principal authentication
    # These can be passed as parameters or loaded from environment variables
    client = AuthenticatedClient(
        base_url="https://api.kythera.com",  # Optional, will use default
        tenant_id="your-tenant-id",         # Optional, will use AZURE_TENANT_ID or "common"
        client_id="your-client-id",         # Required, or set AZURE_CLIENT_ID
        client_secret="your-client-secret", # Optional, if provided will use service principal auth
        timeout=30                          # Optional, default is 30 seconds
    )
    
    try:
        # Check authentication status
        token_info = client.get_token_info()
        print(f"Auth type: {token_info['auth_type']}")
        print(f"Has token: {token_info['has_token']}")
        
        # Make API requests - authentication is handled automatically
        response = client.get("some-endpoint")
        print(f"API Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


def example_device_flow_auth():
    """Example using device flow authentication (without client_secret)."""
    print("=== Device Flow Authentication Example ===")
    
    # Create client with device flow authentication
    # When client_secret is not provided, device flow is used
    client = AuthenticatedClient(
        client_id="your-client-id"  # Only client_id is required for device flow
    )
    
    try:
        # Check authentication status
        token_info = client.get_token_info()
        print(f"Auth type: {token_info['auth_type']}")
        
        # First API request will trigger device flow authentication
        # User will see instructions to authenticate via browser
        response = client.get("some-endpoint")
        print(f"API Response: {response}")
        
        # Subsequent requests will use cached token
        response2 = client.get("another-endpoint")
        print(f"Second API Response: {response2}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


def example_environment_variables():
    """Example using environment variables for configuration."""
    print("=== Environment Variables Example ===")
    
    # Set environment variables (in practice, these would be set in your environment)
    os.environ["AZURE_CLIENT_ID"] = "your-client-id"
    os.environ["AZURE_TENANT_ID"] = "your-tenant-id"
    os.environ["KYTHERA_BASE_URL"] = "https://api.kythera.com"
    # os.environ["AZURE_CLIENT_SECRET"] = "your-client-secret"  # Optional for service principal
    
    # Create client - all configuration loaded from environment
    client = AuthenticatedClient()
    
    try:
        # Use the client
        response = client.get("some-endpoint")
        print(f"API Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


def example_context_manager():
    """Example using the client as a context manager."""
    print("=== Context Manager Example ===")
    
    # Using context manager ensures proper cleanup
    with AuthenticatedClient(client_id="your-client-id") as client:
        try:
            # Check token info
            token_info = client.get_token_info()
            print(f"Authenticated: {not token_info['is_expired']}")
            
            # Make API requests
            response = client.get("some-endpoint")
            print(f"GET Response: {response}")
            
            # POST request example
            post_response = client.post("some-endpoint", data={"key": "value"})
            print(f"POST Response: {post_response}")
            
        except Exception as e:
            print(f"Error: {e}")
    # Client is automatically closed when exiting the context


def example_token_management():
    """Example demonstrating token management features."""
    print("=== Token Management Example ===")
    
    client = AuthenticatedClient(client_id="your-client-id")
    
    try:
        # Get token information
        token_info = client.get_token_info()
        print("Token Info:")
        for key, value in token_info.items():
            print(f"  {key}: {value}")
        
        # Check if authenticated
        if client.is_authenticated():
            print("Client is authenticated with valid token")
        else:
            print("Client needs authentication")
        
        # Clear token cache if needed
        client.clear_token_cache()
        print("Token cache cleared")
        
        # Next API request will acquire a new token
        response = client.get("some-endpoint")
        print(f"API Response after cache clear: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    print("AuthenticatedClient Examples")
    print("=" * 50)
    
    # Uncomment the examples you want to run:
    
    # example_service_principal_auth()
    # example_device_flow_auth()
    # example_environment_variables()
    # example_context_manager()
    # example_token_management()
    
    print("\nTo run these examples:")
    print("1. Set your Azure AD application credentials")
    print("2. Uncomment the example functions you want to test")
    print("3. Replace 'your-client-id', 'your-tenant-id', etc. with actual values")
