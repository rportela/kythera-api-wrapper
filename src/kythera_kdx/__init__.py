"""
Kythera KDX - A Python wrapper for the Kythera API

This package provides a convenient Python interface to interact with the Kythera API.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .client import KytheraClient
from .exceptions import KytheraError, KytheraAPIError, KytheraAuthError
from .utils import get_api_key_from_env, validate_api_key, format_endpoint

__all__ = [
    "KytheraClient",
    "KytheraError", 
    "KytheraAPIError",
    "KytheraAuthError",
    "get_api_key_from_env",
    "validate_api_key",
    "format_endpoint",
]
