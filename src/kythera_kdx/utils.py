"""
Utility functions and helpers for the Kythera KDX package.
"""

import os
from typing import Optional


def get_api_key_from_env() -> Optional[str]:
    """
    Get the API key from environment variables.
    
    Checks for KYTHERA_API_KEY environment variable.
    
    Returns:
        API key if found, None otherwise
    """
    return os.getenv("KYTHERA_API_KEY")


def validate_api_key(api_key: str) -> bool:
    """
    Validate the format of an API key.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        True if the API key appears valid, False otherwise
    """
    if not api_key or not isinstance(api_key, str):
        return False
    
    # Basic validation - adjust based on actual Kythera API key format
    return len(api_key.strip()) > 0


def format_endpoint(endpoint: str) -> str:
    """
    Format an API endpoint to ensure it starts with a forward slash.
    
    Args:
        endpoint: The endpoint to format
        
    Returns:
        Formatted endpoint
    """
    if not endpoint:
        return "/"
    
    endpoint = endpoint.strip()
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    
    return endpoint
