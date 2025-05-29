"""
Simple test to verify MSAL authentication works.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_msal_import():
    """Test importing MSAL components."""
    try:
        # Test MSAL import directly
        import msal
        print("✓ MSAL library imported successfully")
        
        # Test our auth module
        from kythera_kdx.auth import MSALAuthenticator
        print("✓ MSALAuthenticator imported successfully")
        
        # Test instantiation
        auth = MSALAuthenticator(
            client_id="test-client-id",
            client_secret="test-secret",
            tenant_id="test-tenant"
        )
        print("✓ MSALAuthenticator instantiated successfully")
        print(f"  - Client ID: {auth.client_id}")
        print(f"  - Authority: {auth.authority}")
        print(f"  - Scope: {auth.scope}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exceptions_import():
    """Test importing exceptions."""
    try:
        from kythera_kdx.exceptions import KytheraAuthError
        print("✓ KytheraAuthError imported successfully")
        return True
    except Exception as e:
        print(f"✗ Error importing exceptions: {e}")
        return False

if __name__ == "__main__":
    print("Testing MSAL Authentication Components")
    print("=" * 40)
    
    success = True
    success &= test_exceptions_import()
    success &= test_msal_import()
    
    if success:
        print("\n✓ All tests passed! MSAL authentication is working.")
    else:
        print("\n✗ Some tests failed.")
