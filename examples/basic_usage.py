"""
Example usage of the Kythera KDX library.

This script demonstrates basic usage of the KytheraClient.
"""

from kythera_kdx import KytheraClient, KytheraAPIError, KytheraAuthError
import os


def main():
    """Main example function."""
    
    # Example 1: Initialize with API key from environment
    print("=== Example 1: Client with environment API key ===")
    try:
        client = KytheraClient()
        if client.api_key:
            print("✓ Client initialized with API key from environment")
        else:
            print("⚠ No API key found in environment (KYTHERA_API_KEY)")
    except Exception as e:
        print(f"✗ Error initializing client: {e}")
    
    # Example 2: Initialize with explicit API key
    print("\n=== Example 2: Client with explicit API key ===")
    try:
        client = KytheraClient(api_key="your-api-key-here")
        print("✓ Client initialized with explicit API key")
    except Exception as e:
        print(f"✗ Error initializing client: {e}")
    
    # Example 3: Making API requests (mock example)
    print("\n=== Example 3: Making API requests ===")
    client = KytheraClient(api_key="test-key")
    
    try:
        # This would be a real API call
        # response = client.get("/users")
        # print(f"✓ GET request successful: {response}")
        print("ℹ Skipping real API call - replace with actual endpoint")
        
    except KytheraAuthError:
        print("✗ Authentication failed - check your API key")
    except KytheraAPIError as e:
        print(f"✗ API error: {e.status_code} - {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Example 4: POST request with data
    print("\n=== Example 4: POST request example ===")
    try:
        data = {
            "name": "Test User",
            "email": "test@example.com"
        }
        # response = client.post("/users", data=data)
        # print(f"✓ POST request successful: {response}")
        print("ℹ Skipping real API call - replace with actual endpoint")
        
    except Exception as e:
        print(f"✗ Error in POST request: {e}")
    
    print("\n=== Example complete ===")
    print("Remember to:")
    print("1. Set your actual API key in the KYTHERA_API_KEY environment variable")
    print("2. Replace example endpoints with real Kythera API endpoints")
    print("3. Handle errors appropriately in your production code")


if __name__ == "__main__":
    main()
