import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from kythera_kdx import (
        KytheraClient, AddInClient, FundsClient, GlobalsClient,
        InstrumentGroupsClient, InstrumentsClient, InstrumentParametersClient,
        IntradayClient, PnlClient, PositionsClient, PricesClient,
        RiskFactorsClient, TradesClient
    )
    print("SUCCESS: All 13 client classes imported successfully")
    
    main_client = KytheraClient(api_key="test-key")
    clients = [
        AddInClient(main_client),
        FundsClient(main_client),
        GlobalsClient(main_client),
        InstrumentGroupsClient(main_client),
        InstrumentsClient(main_client),
        InstrumentParametersClient(main_client),
        IntradayClient(main_client),
        PnlClient(main_client),
        PositionsClient(main_client),
        PricesClient(main_client),
        RiskFactorsClient(main_client),
        TradesClient(main_client),
    ]
    print(f"SUCCESS: All {len(clients)} client instances created successfully")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
