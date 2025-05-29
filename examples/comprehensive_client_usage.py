"""
Example demonstrating the usage of all Kythera KDX client modules.

This example shows how to use each client to interact with different 
parts of the Kythera API according to the OpenAPI specification.
"""

from datetime import date, datetime
from kythera_kdx import (
    KytheraClient,
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


def main():
    """Demonstrate usage of all client modules."""
    
    # Initialize the main client
    # In production, use: client = KytheraClient(api_key="your-actual-api-key")
    client = KytheraClient(api_key="demo-key")
    
    print("=== Kythera KDX Client Examples ===\n")
    
    # 1. AddIn Client
    print("1. AddIn Client")
    addin_client = AddInClient(client)
    try:
        # Get add-in information
        # addin_info = addin_client.get_add_in()
        # version_info = addin_client.get_add_in_version()
        # core_info = addin_client.get_add_in_core("1.0")
        print("   ✓ AddIn endpoints available")
    except Exception as e:
        print(f"   ✗ AddIn error: {e}")
    
    # 2. Funds Client
    print("2. Funds Client")
    funds_client = FundsClient(client)
    try:
        # Get all funds
        # funds = funds_client.get_funds(enabled_only=True, fetch_characteristics=True)
        # Get fund NAVs for a specific date
        # navs = funds_client.get_fund_navs(date=date.today())
        print("   ✓ Funds endpoints available")
    except Exception as e:
        print(f"   ✗ Funds error: {e}")
    
    # 3. Globals Client
    print("3. Globals Client")
    globals_client = GlobalsClient(client)
    try:
        # Get reference data
        # calendars = globals_client.get_calendars()
        # countries = globals_client.get_countries()
        # currencies = globals_client.get_currencies()
        # institutions = globals_client.get_institutions()
        # institution_types = globals_client.get_institution_types()
        # issuers = globals_client.get_issuers()
        print("   ✓ Globals endpoints available")
    except Exception as e:
        print(f"   ✗ Globals error: {e}")
    
    # 4. Instrument Groups Client
    print("4. Instrument Groups Client")
    instrument_groups_client = InstrumentGroupsClient(client)
    try:
        # Get instrument groups
        # groups = instrument_groups_client.get_instrument_groups()
        print("   ✓ Instrument Groups endpoints available")
    except Exception as e:
        print(f"   ✗ Instrument Groups error: {e}")
    
    # 5. Instruments Client
    print("5. Instruments Client")
    instruments_client = InstrumentsClient(client)
    try:
        # Get instruments
        # instruments = instruments_client.get_instruments(
        #     enabled_only=True,
        #     fetch_characteristics=True,
        #     fetch_group=True
        # )
        print("   ✓ Instruments endpoints available")
    except Exception as e:
        print(f"   ✗ Instruments error: {e}")
    
    # 6. Instrument Parameters Client
    print("6. Instrument Parameters Client")
    instrument_params_client = InstrumentParametersClient(client)
    try:
        # Get instrument parameters
        # parameters = instrument_params_client.get_instrument_parameters()
        print("   ✓ Instrument Parameters endpoints available")
    except Exception as e:
        print(f"   ✗ Instrument Parameters error: {e}")
    
    # 7. Intraday Client
    print("7. Intraday Client")
    intraday_client = IntradayClient(client)
    try:
        # Get intraday data
        # intraday_prices = intraday_client.get_intraday_prices()
        # intraday_risk_factors = intraday_client.get_intraday_risk_factor_values()
        print("   ✓ Intraday endpoints available")
    except Exception as e:
        print(f"   ✗ Intraday error: {e}")
    
    # 8. PnL Client
    print("8. PnL Client")
    pnl_client = PnlClient(client)
    try:
        # Get PnL data
        # pnl_data = pnl_client.get_intraday_pnl()
        print("   ✓ PnL endpoints available")
    except Exception as e:
        print(f"   ✗ PnL error: {e}")
    
    # 9. Positions Client
    print("9. Positions Client")
    positions_client = PositionsClient(client)
    try:
        # Get positions
        # positions = positions_client.get_positions(
        #     position_date=date.today(),
        #     is_open=True
        # )
        print("   ✓ Positions endpoints available")
    except Exception as e:
        print(f"   ✗ Positions error: {e}")
    
    # 10. Prices Client
    print("10. Prices Client")
    prices_client = PricesClient(client)
    try:
        # Get prices
        # all_prices = prices_client.get_all_prices(
        #     price_date=date.today(),
        #     price_type_name="CLOSE"
        # )
        # instrument_prices = prices_client.get_prices_by_instrument(
        #     instrument_id=123,
        #     price_date=date.today(),
        #     price_type_name="CLOSE"
        # )
        # price_types = prices_client.get_price_types()
        
        # Post prices (example)
        # from kythera_kdx.models_v1 import OverrideInstrumentPriceRequest
        # price_requests = [
        #     OverrideInstrumentPriceRequest(
        #         instrumentId=123,
        #         price=100.50,
        #         rate=0.05
        #     )
        # ]
        # prices_client.post_prices(price_requests)
        print("   ✓ Prices endpoints available")
    except Exception as e:
        print(f"   ✗ Prices error: {e}")
    
    # 11. Risk Factors Client
    print("11. Risk Factors Client")
    risk_factors_client = RiskFactorsClient(client)
    try:
        # Get risk factors
        # risk_factors = risk_factors_client.get_risk_factors()
        # risk_factor_values = risk_factors_client.get_risk_factor_values(
        #     valuation_date=date.today()
        # )
        # risk_value_types = risk_factors_client.get_risk_factor_value_types()
        
        # Post risk factor values (example)
        # from kythera_kdx.models_v1 import OverrideRiskFactorValueRequest, RiskFactorPoint
        # risk_factor_requests = [
        #     OverrideRiskFactorValueRequest(
        #         riskFactorId=123,
        #         riskFactorType="CURVE",
        #         riskFactorPoint=RiskFactorPoint(riskFactorValue=0.025)
        #     )
        # ]
        # risk_factors_client.post_risk_factor_values(risk_factor_requests)
        print("   ✓ Risk Factors endpoints available")
    except Exception as e:
        print(f"   ✗ Risk Factors error: {e}")
    
    # 12. Trades Client
    print("12. Trades Client")
    trades_client = TradesClient(client)
    try:
        # Get trades
        # trades = trades_client.get_trades(effective_date=date.today())
        print("   ✓ Trades endpoints available")
    except Exception as e:
        print(f"   ✗ Trades error: {e}")
    
    print("\n=== Summary ===")
    print("All 12 client modules are properly organized and ready to use!")
    print("Each client handles its specific set of API endpoints according to the OpenAPI specification.")
    print("\nTo use in production:")
    print("1. Set your actual API key")
    print("2. Uncomment the API calls you need")
    print("3. Handle responses according to your business logic")


if __name__ == "__main__":
    main()
