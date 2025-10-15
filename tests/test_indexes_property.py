"""Test script to verify that the indexes property works correctly in KytheraKdx."""

import sys
import os
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_indexes_property_without_auth():
    """Test that indexes property is accessible without authentication."""
    from kythera_kdx import KytheraKdx
    from kythera_kdx.indexes import IndexesClient
    
    # Mock the authentication to avoid real API calls
    with patch('kythera_kdx.authenticated_client.ConfidentialClientApplication'):
        with patch('kythera_kdx.authenticated_client.PublicClientApplication'):
            # Create instance without triggering actual auth
            kdx = KytheraKdx.__new__(KytheraKdx)
            
            # Manually initialize the private attributes
            kdx._indexes_client = None
            kdx._base_url = "https://test.com"
            kdx._timeout = 30
            
            # Test that indexes property can be accessed
            assert hasattr(kdx, 'indexes'), "KytheraKdx missing 'indexes'"
            
            # Test that accessing the property returns an IndexesClient
            indexes = kdx.indexes
            assert isinstance(indexes, IndexesClient), \
                f"Expected IndexesClient, got {type(indexes)}"
            
            # Test lazy loading
            indexes2 = kdx.indexes
            assert indexes is indexes2, "Lazy loading failed"
            
            print("✅ All tests passed!")
            print("✓ kdx.indexes property is accessible")
            print("✓ kdx.indexes returns IndexesClient instance")
            print("✓ Lazy loading works correctly")
            
            return True


if __name__ == "__main__":
    try:
        success = test_indexes_property_without_auth()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
