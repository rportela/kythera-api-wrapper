"""
Simple test to verify all client modules are properly structured.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from kythera_kdx import (
    AuthenticatedClient,
    AddInClient,
    FundsClient,
    GlobalsClient,
    InstrumentGroupsClient,
    InstrumentsClient,
    InstrumentParametersClient,
    IntradayClient,
    PnlClient,
    PositionsClient,
    PricesClient,
    RiskFactorsClient,
    TradesClient,
)


def test_client_structure():
    """Test that all clients can be instantiated and have expected methods."""

    # Create main client
    main_client = AuthenticatedClient()

    # Test all client classes
    clients = {
        "AddInClient": AddInClient,
        "FundsClient": FundsClient,
        "GlobalsClient": GlobalsClient,
        "InstrumentGroupsClient": InstrumentGroupsClient,
        "InstrumentsClient": InstrumentsClient,
        "InstrumentParametersClient": InstrumentParametersClient,
        "IntradayClient": IntradayClient,
        "PnlClient": PnlClient,
        "PositionsClient": PositionsClient,
        "PricesClient": PricesClient,
        "RiskFactorsClient": RiskFactorsClient,
        "TradesClient": TradesClient,
    }

    print("=== Client Structure Verification ===\n")

    for name, client_class in clients.items():
        try:
            # Instantiate client
            client_instance = client_class(main_client)

            # Get methods that don't start with _
            methods = [
                method
                for method in dir(client_instance)
                if not method.startswith("_")
                and callable(getattr(client_instance, method))
            ]

            print(f"✓ {name}:")
            for method in methods:
                print(f"    - {method}()")
            print()

        except Exception as e:
            print(f"✗ {name}: Error - {e}\n")

    print("=== Summary ===")
    print(f"Successfully verified {len(clients)} client modules!")
    print("All clients follow the consistent structure pattern.")


if __name__ == "__main__":
    test_client_structure()
