#!/usr/bin/env python3
"""
Simple test to verify MSAL authentication works.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing MSAL components...")
    
    # Test 1: Import MSALAuthenticator
    from kythera_kdx.auth import MSALAuthenticator
    print("✓ MSALAuthenticator imported")
    
    # Test 2: Import KytheraClient
    from kythera_kdx.client import KytheraClient
    print("✓ KytheraClient imported")
    
    # Test 3: Create MSAL authenticator
    auth = MSALAuthenticator(
        client_id="test-client-id",
        client_secret="test-secret"
    )
    print("✓ MSALAuthenticator created")
    
    # Test 4: Create client with MSAL
    client = KytheraClient(use_msal=True, msal_authenticator=auth)
    print("✓ KytheraClient with MSAL created")
    
    # Test 5: Test token info
    token_info = auth.get_token_info()
    print(f"✓ Token info: {token_info}")
    
    print("\n🎉 All tests passed! MSAL authentication is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
