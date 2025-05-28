"""
Custom exceptions for the Kythera KDX package.
"""


class KytheraError(Exception):
    """Base exception class for all Kythera-related errors."""
    pass


class KytheraAPIError(KytheraError):
    """Exception raised when the Kythera API returns an error response."""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class KytheraAuthError(KytheraError):
    """Exception raised when authentication with the Kythera API fails."""
    pass


class KytheraConnectionError(KytheraError):
    """Exception raised when connection to the Kythera API fails."""
    pass


class KytheraTimeoutError(KytheraError):
    """Exception raised when a request to the Kythera API times out."""
    pass
