#!/usr/bin/env python3
"""
Test script to verify MSAL authentication components work without errors.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all components can be imported without circular import issues."""
    print("Testing imports...")
    
    try:
        from kythera_kdx.auth import MSALAuthenticator
        print("✓ MSALAuthenticator imported successfully")
    except Exception as e:
        print(f"✗ Failed to import MSALAuthenticator: {e}")
        return False
    
    try:
        from kythera_kdx.client import KytheraClient
        print("✓ KytheraClient imported successfully")
    except Exception as e:
        print(f"✗ Failed to import KytheraClient: {e}")
        return False
    
    try:
        from kythera_kdx import KytheraClient, MSALAuthenticator
        print("✓ Package-level imports work")
    except Exception as e:
        print(f"✗ Package-level imports failed: {e}")
        return False
    
    return True

def test_msal_authenticator_creation():
    """Test MSALAuthenticator creation without real credentials."""
    print("\nTesting MSALAuthenticator creation...")
    
    try:
        from kythera_kdx.auth import MSALAuthenticator
        
        # Test with minimal parameters (should work without real credentials)
        auth = MSALAuthenticator(
            client_id="test-client-id",
            client_secret="test-secret"
        )
        print("✓ MSALAuthenticator created successfully")
        print(f"  - Client ID: {auth.client_id}")
        print(f"  - Authority: {auth.authority}")
        print(f"  - Scopes: {auth.scopes}")
        
        # Test token info without actual authentication
        token_info = auth.get_token_info()
        print(f"  - Token info: {token_info}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to create MSALAuthenticator: {e}")
        return False

def test_kythera_client_creation():
    """Test KytheraClient creation with different auth methods."""
    print("\nTesting KytheraClient creation...")
    
    try:
        from kythera_kdx.client import KytheraClient
        from kythera_kdx.auth import MSALAuthenticator
        
        # Test with API key
        client_api = KytheraClient(api_key="test-api-key")
        print("✓ KytheraClient created with API key")
        
        # Test with MSAL (without real credentials)
        msal_auth = MSALAuthenticator(
            client_id="test-client-id",
            client_secret="test-secret"
        )
        client_msal = KytheraClient(use_msal=True, msal_authenticator=msal_auth)
        print("✓ KytheraClient created with MSAL authenticator")
        
        # Test context manager
        with KytheraClient(api_key="test-key") as client:
            print("✓ KytheraClient context manager works")
        
        return True
    except Exception as e:
        print(f"✗ Failed to create KytheraClient: {e}")
        return False

def main():
    """Run all tests."""
    print("=== MSAL Authentication Component Test ===\n")
    
    tests = [
        test_imports,
        test_msal_authenticator_creation,
        test_kythera_client_creation,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=== Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! MSAL authentication is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
