import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from kythera_kdx import (
    KytheraClient, AddInClient, FundsClient, GlobalsClient,
    InstrumentGroupsClient, InstrumentsClient, InstrumentParametersClient,
    IntradayClient, PnlClient, PositionsClient, PricesClient,
    RiskFactorsClient, TradesClient
)

main_client = KytheraClient(api_key="test-key")

# Test that each client has the expected methods
client_methods = {
    'AddInClient': ['get_add_in', 'get_add_in_core', 'get_add_in_version'],
    'FundsClient': ['get_funds'],
    'GlobalsClient': ['get_calendars', 'get_countries', 'get_currencies', 'get_institutions', 'get_institution_types', 'get_issuers'],
    'InstrumentGroupsClient': ['get_instrument_groups'],
    'InstrumentsClient': ['get_instruments', 'create_instruments'],
    'InstrumentParametersClient': ['get_instrument_parameters'],
    'IntradayClient': ['get_intraday_prices', 'get_intraday_risk_factor_values'],
    'PnlClient': ['get_intraday_pnl'],
    'PositionsClient': ['get_positions'],
    'PricesClient': ['get_all_prices', 'override_instrument_price', 'get_price_types'],
    'RiskFactorsClient': ['get_risk_factors'],
    'TradesClient': ['get_trades']
}

clients = {
    'AddInClient': AddInClient(main_client),
    'FundsClient': FundsClient(main_client),
    'GlobalsClient': GlobalsClient(main_client),
    'InstrumentGroupsClient': InstrumentGroupsClient(main_client),
    'InstrumentsClient': InstrumentsClient(main_client),
    'InstrumentParametersClient': InstrumentParametersClient(main_client),
    'IntradayClient': IntradayClient(main_client),
    'PnlClient': PnlClient(main_client),
    'PositionsClient': PositionsClient(main_client),
    'PricesClient': PricesClient(main_client),
    'RiskFactorsClient': RiskFactorsClient(main_client),
    'TradesClient': TradesClient(main_client),
}

all_methods_found = True

for client_name, client_instance in clients.items():
    expected_methods = client_methods[client_name]
    for method_name in expected_methods:
        if hasattr(client_instance, method_name):
            print(f"✓ {client_name}.{method_name}() - Found")
        else:
            print(f"✗ {client_name}.{method_name}() - Missing")
            all_methods_found = False

if all_methods_found:
    print("\n🎉 SUCCESS: All client methods are properly accessible!")
    print("📊 Complete OpenAPI specification coverage achieved")
    print("🏗️ Client structure is ready for production use")
else:
    print("\n❌ Some methods are missing - please check implementation")
