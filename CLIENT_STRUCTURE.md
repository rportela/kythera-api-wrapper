# Kythera KDX Client Structure

This document outlines the complete client module structure organized by API paths and endpoints.

## Client Organization

### 1. AddInClient (`addin.py`)
**Base Path:** `/add-in`

**Methods:**
- `get_add_in()` → `GET /add-in`
- `get_add_in_core(version: str)` → `GET /add-in/core?version={version}`
- `get_add_in_version()` → `GET /add-in/version`

### 2. FundsClient (`funds.py`)
**Base Path:** `/v1/funds`

**Methods:**
- `get_funds(enabled_only=True, fetch_characteristics=True)` → `GET /v1/funds`
- `get_fund_navs(date=None, start_date=None, end_date=None, fund_id=None)` → `GET /v1/funds/navs`

### 3. GlobalsClient (`globals.py`)
**Base Path:** `/v1/globals`

**Methods:**
- `get_calendars()` → `GET /v1/globals/calendars`
- `get_countries()` → `GET /v1/globals/countries`
- `get_currencies()` → `GET /v1/globals/currencies`
- `get_institutions(fetch_characteristics=False, fetch_nomenclatures=False)` → `GET /v1/globals/institutions`
- `get_institution_types()` → `GET /v1/globals/institutions/types`
- `get_issuers(fetch_characteristics=False)` → `GET /v1/globals/issuers`

### 4. InstrumentGroupsClient (`instrument_groups.py`)
**Base Path:** `/v1/instrument-groups`

**Methods:**
- `get_instrument_groups(fetch_characteristics=True, fetch_nomenclatures=True)` → `GET /v1/instrument-groups`

### 5. InstrumentsClient (`instruments.py`)
**Base Path:** `/v1/instruments`

**Methods:**
- `get_instruments(enabled_only=True, fetch_characteristics=True, fetch_group=True)` → `GET /v1/instruments`

### 6. InstrumentParametersClient (`instrument_parameters.py`)
**Base Path:** `/v1/instruments/parameters`

**Methods:**
- `get_instrument_parameters()` → `GET /v1/instruments/parameters`

### 7. IntradayClient (`intraday.py`)
**Base Path:** `/v1/intraday-*`

**Methods:**
- `get_intraday_prices()` → `GET /v1/intraday-prices`
- `get_intraday_risk_factor_values()` → `GET /v1/intraday-risk-factor-values`

### 8. PnlClient (`pnl.py`)
**Base Path:** `/v1/pnl`

**Methods:**
- `get_intraday_pnl()` → `GET /v1/pnl/intraday`

### 9. PositionsClient (`positions.py`)
**Base Path:** `/v1/positions`

**Methods:**
- `get_positions(position_date=None, is_open=True)` → `GET /v1/positions`

### 10. PricesClient (`prices.py`)
**Base Path:** `/v1/prices`

**Methods:**
- `get_all_prices(price_date, price_type_name)` → `GET /v1/prices`
- `get_prices_by_instrument(instrument_id, price_date, price_type_name)` → `GET /v1/prices/{instrumentId}`
- `post_prices(requests)` → `POST /v1/prices`
- `get_price_types()` → `GET /v1/prices/price-types`

### 11. RiskFactorsClient (`risk_factors.py`)
**Base Path:** `/v1/risk-factor*`

**Methods:**
- `get_risk_factors()` → `GET /v1/risk-factors`
- `get_risk_factor_values(valuation_date)` → `GET /v1/risk-factor-values`
- `post_risk_factor_values(requests)` → `POST /v1/risk-factor-values`
- `get_risk_factor_value_types()` → `GET /v1/risk-factor-values/types`

### 12. TradesClient (`trades.py`)
**Base Path:** `/v1/trades`

**Methods:**
- `get_trades(effective_date=None)` → `GET /v1/trades`

## Usage Example

```python
from kythera_kdx import KytheraClient, FundsClient, PricesClient

# Initialize the main client
client = KytheraClient(api_key="your-api-key")

# Use specific resource clients
funds_client = FundsClient(client)
prices_client = PricesClient(client)

# Get all funds
funds = funds_client.get_funds()

# Get prices for a specific date
from datetime import date
prices = prices_client.get_all_prices(
    price_date=date.today(),
    price_type_name="CLOSE"
)
```

## Coverage Summary

✅ **Complete Coverage** - All endpoints from the OpenAPI specification are implemented across the client modules:

- **3** AddIn endpoints
- **2** Funds endpoints  
- **6** Globals endpoints
- **1** Instrument Groups endpoint
- **1** Instruments endpoint
- **1** Instrument Parameters endpoint
- **2** Intraday endpoints
- **1** PnL endpoint
- **1** Positions endpoint
- **4** Prices endpoints (3 GET, 1 POST)
- **4** Risk Factors endpoints (3 GET, 1 POST)
- **1** Trades endpoint

**Total: 27 endpoints** organized across **12 client modules**

## Architecture Benefits

1. **Logical Organization** - Endpoints grouped by business domain
2. **Type Safety** - All methods use Pydantic models for request/response data
3. **Consistency** - All clients follow the same initialization and method patterns
4. **Extensibility** - Easy to add new endpoints to existing clients
5. **Maintainability** - Clear separation of concerns between different API areas
