"""
Kythera KDX - A Python wrapper for the Kythera API

This package provides a convenient Python interface to interact with the Kythera API.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .client import KytheraClient
from .auth import MSALAuthenticator
from .exceptions import KytheraError, KytheraAPIError, KytheraAuthError
from .utils import get_api_key_from_env, validate_api_key, format_endpoint
from .addin import AddInClient
from .funds import FundsClient
from .globals import GlobalsClient
from .instrument_groups import InstrumentGroupsClient
from .instrument_parameters import InstrumentParametersClient
from .instruments import InstrumentsClient
from .intraday import IntradayClient
from .pnl import PnlClient
from .prices import PricesClient
from .risk_factors import RiskFactorsClient
from .positions import PositionsClient
from .trades import TradesClient

__all__ = [
    "KytheraClient",
    "KytheraError", 
    "KytheraAPIError",
    "KytheraAuthError",
    "get_api_key_from_env",
    "validate_api_key",
    "format_endpoint",
    "AddInClient",
    "FundsClient",
    "GlobalsClient",
    "InstrumentGroupsClient",
    "InstrumentParametersClient",    "InstrumentsClient",
    "IntradayClient",
    "PnlClient",
    "PricesClient",
    "RiskFactorsClient",
    "PositionsClient",
    "TradesClient",
]
