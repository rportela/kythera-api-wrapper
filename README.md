# Kythera KDX

A Python wrapper for the Kythera Data eXchange (KDX) API that provides a comprehensive interface for accessing financial and investment management data. This library enables portfolio managers, fund administrators, and financial professionals to programmatically interact with Kythera's investment management platform.

## Installation

```bash
pip install kythera-kdx     
```

## Quick Start

```python
from kythera_kdx import KytheraKdx
from datetime import date

# Initialize the unified client
kdx = KytheraKdx(
    x_api_key="xxxx-xxxx-xxxx",  # <-- API key authentication
    client_id="your-client-id",  # Optional - for OAuth2
    client_secret="your-client-secret",  # Optional
    tenant_id="your-tenant-id"    # Optional
)

# Get fund information
funds = kdx.funds.get_funds(enabled_only=True)

# Get current open positions
positions = kdx.positions.get_positions(is_open=True)

# Get intraday P&L
pnl = kdx.pnl.get_intraday_pnl_df()

print(f"Found {len(funds)} funds, {len(positions)} positions")
print(f"Current P&L: {pnl['pnl'].sum():.2f}")
```

## Features

- 📊 **Comprehensive Financial Data Access** - Funds, instruments, positions, trades, and P&L data
- 💰 **Portfolio Management** - Real-time position tracking and fund administration
- 📈 **Market Data** - Pricing information and risk factor data
- 🔐 **Secure Authentication** - Built-in API key and OAuth2 support
- 🛡️ **Robust Error Handling** - Comprehensive exception classes for different error types
- 📝 **Full Type Safety** - Complete type hints for all data models
- ✅ **Production Ready** - Extensive test coverage and validation
- 🚀 **Easy Integration** - Simple, intuitive API design

## Authentication

The library supports two Azure AD authentication methods:

### Service Principal Authentication (Recommended for Production)

```python
from kythera_kdx import KytheraKdx

kdx = KytheraKdx(
    client_id="your-app-registration-client-id",
    client_secret="your-app-registration-client-secret",
    tenant_id="your-azure-tenant-id"
)
```

### Device Flow Authentication (For Development/Testing)

```python
from kythera_kdx import KytheraKdx

# This will prompt you to visit a URL and enter a device code
kdx = KytheraKdx(
    client_id="your-app-registration-client-id",
    tenant_id="your-azure-tenant-id"
    # No client_secret - triggers device flow
)
```

### API Key Authentication (Simple)

```python
from kythera_kdx import KytheraKdx

kdx = KytheraKdx(x_api_key="xxxx-xxxx-xxxx")
```

## Authentication and Environment Variables

The client reads configuration from parameters or environment variables:

- KYTHERA_BASE_URL (default: https://kdx-api.app.lgcy.com.br)
- KYTHERA_TENANT_ID (default: 497a1564-7d5b-48d3-a55e-791eaeef5819)
- KYTHERA_CLIENT_ID (required if not passed as parameter)
- KYTHERA_CLIENT_SECRET (optional; when set, uses service principal)
- KYTHERA_SCOPES (optional; default: "{client_id}/.default")
- KYTHERA_X_API_KEY (optional; adds X-Api-Key header in addition to Authorization)

Scopes guidance:
- By default we request the application default scope using the pattern {client_id}/.default.
- If your Azure AD app exposes a custom resource URI (api://.../access), set KYTHERA_SCOPES to that value.

### Environment Variables

You can set your authentication credentials using environment variables:

```bash
export KYTHERA_CLIENT_ID="your-client-id"
export KYTHERA_CLIENT_SECRET="your-client-secret"
export KYTHERA_TENANT_ID="your-tenant-id"
export KYTHERA_X_API_KEY="xxxx-xxxx-xxxx"
```

### Client Configuration

```python
from kythera_kdx import KytheraKdx

# Service principal authentication (recommended for production)
kdx = KytheraKdx(
    client_id="your-client-id",
    client_secret="your-client-secret",
    tenant_id="your-tenant-id",
    base_url="https://api.kythera.com",  # Optional, uses default
    timeout=30  # Optional, request timeout in seconds
)

# Interactive device flow authentication (for development/testing)
kdx = KytheraKdx(
    client_id="your-client-id",
    tenant_id="your-tenant-id"
    # No client_secret for device flow
)

# API key authentication (simple)
kdx = KytheraKdx(
    x_api_key="xxxx-xxxx-xxxx"
)
```

## Usage Examples

### Comprehensive Example

```python
from kythera_kdx import KytheraKdx
from datetime import date
import pandas as pd

# Initialize the unified client
kdx = KytheraKdx(
    x_api_key="xxxx-xxxx-xxxx",  # <-- API key authentication
    client_id="your-client-id",
    client_secret="your-client-secret", 
    tenant_id="your-tenant-id"
)

# Get all data as DataFrames for analysis
print("📊 Fetching comprehensive portfolio data...")

# Funds and NAVs
funds_df = kdx.funds.get_funds_df(enabled_only=True)
navs_df = kdx.funds.get_fund_navs_df(date=date.today())

# Positions and P&L
positions_df = kdx.positions.get_positions_df(is_open=True)
pnl_df = kdx.pnl.get_intraday_pnl_df()

# Market data
prices_df = kdx.prices.get_all_prices_df(
    price_date=date.today(),
    price_type_name="CLOSE"
)
intraday_prices_df = kdx.intraday.get_intraday_prices_df()

# Trading activity
trades_df = kdx.trades.get_trades_df(effective_date=date.today())

# Analysis
print(f"📈 Portfolio Summary:")
print(f"   Active Funds: {len(funds_df)}")
print(f"   Open Positions: {len(positions_df)}")
print(f"   Today's Trades: {len(trades_df)}")
print(f"   Current P&L: ${pnl_df['pnl'].sum():,.2f}")
print(f"   Total AUM: ${navs_df['value'].sum():,.2f}")

# Top performing instruments by P&L
top_performers = pnl_df.nlargest(5, 'pnl')[['instrumentName', 'pnl']]
print(f"\n🏆 Top 5 Performers Today:")
for _, row in top_performers.iterrows():
    print(f"   {row['instrumentName']}: ${row['pnl']:,.2f}")
```

### Working with Funds

```python
from kythera_kdx import KytheraKdx
from datetime import date

kdx = KytheraKdx(x_api_key="xxxx-xxxx-xxxx", client_id="your-client-id", client_secret="your-client-secret", tenant_id="your-tenant-id")

# Get all enabled funds with characteristics
funds = kdx.funds.get_funds(enabled_only=True, fetch_characteristics=True)
for fund in funds:
    print(f"Fund: {fund.fullName} ({fund.shortName})")

# Get fund NAVs for today
navs = kdx.funds.get_fund_navs(date=date.today())
for nav in navs:
    print(f"Fund {nav.fundName}: {nav.value} on {nav.date}")

# Get funds as a pandas DataFrame
funds_df = kdx.funds.get_funds_df(enabled_only=True)
print(f"Total funds: {len(funds_df)}")
```

### Portfolio Positions

```python
from kythera_kdx import KytheraKdx
from datetime import date

kdx = KytheraKdx(x_api_key="xxxx-xxxx-xxxx", client_id="your-client-id", client_secret="your-client-secret", tenant_id="your-tenant-id")

# Get current open positions
positions = kdx.positions.get_positions(is_open=True)
for position in positions:
    print(f"Position: {position.instrumentName} - Quantity: {position.quantity}")

# Get positions for a specific date
historical_positions = kdx.positions.get_positions(
    position_date=date(2024, 1, 15),
    is_open=False
)

# Get positions as a pandas DataFrame
positions_df = kdx.positions.get_positions_df(is_open=True)
print(f"Total open positions: {len(positions_df)}")
```

### Trading Data

```python
from kythera_kdx import KytheraKdx
from datetime import date

kdx = KytheraKdx(x_api_key="xxxx-xxxx-xxxx", client_id="your-client-id", client_secret="your-client-secret", tenant_id="your-tenant-id")

# Get trades for today
trades = kdx.trades.get_trades(effective_date=date.today())
for trade in trades:
    print(f"Trade: {trade.instrumentName} - {trade.quantity} @ {trade.price}")

# Get trades as a pandas DataFrame for analysis
trades_df = kdx.trades.get_trades_df(effective_date=date.today())
total_volume = trades_df['notional'].sum()
print(f"Total trading volume: {total_volume:.2f}")
```

### Market Prices and Risk Data

```python
from kythera_kdx import KytheraKdx
from datetime import date

kdx = KytheraKdx(x_api_key="xxxx-xxxx-xxxx", client_id="your-client-id", client_secret="your-client-secret", tenant_id="your-tenant-id")

# Get pricing data for today
prices = kdx.prices.get_all_prices(
    price_date=date.today(),
    price_type_name="CLOSE"
)

# Get prices as DataFrame for analysis
prices_df = kdx.prices.get_all_prices_df(
    price_date=date.today(),
    price_type_name="CLOSE"
)

# Get risk factor values
risk_factors = kdx.risk_factors.get_risk_factor_values(valuation_date=date.today())

# Get intraday pricing data
intraday_prices = kdx.intraday.get_intraday_prices_df()
print(f"Current market prices for {len(intraday_prices)} instruments")
```

### P&L Analysis

```python
from kythera_kdx import KytheraKdx

kdx = KytheraKdx(x_api_key="xxxx-xxxx-xxxx", client_id="your-client-id", client_secret="your-client-secret", tenant_id="your-tenant-id")

# Get current intraday P&L as pandas DataFrame
intraday_pnl_df = kdx.pnl.get_intraday_pnl_df()
print(f"Total P&L: {intraday_pnl_df['pnl'].sum():.2f}")

# Get detailed P&L breakdown
pnl_entries = kdx.pnl.get_intraday_pnl()
for entry in pnl_entries[:5]:  # Show first 5 entries
    print(f"Instrument: {entry.instrumentName} - P&L: {entry.pnl:.2f}")

# Analyze P&L by fund
pnl_by_fund = intraday_pnl_df.groupby('fundName')['pnl'].sum()
print("P&L by Fund:")
print(pnl_by_fund)
```

### Additional examples

# PnL Explain
from datetime import date
start = date(2025, 8, 1)
end = date(2025, 8, 19)
explain = kdx.pnl.get_pnl_explain(start, end, fund_family="MASTER", discriminators=["fundName","instrumentName"])

# Indexes values
vals_today = kdx.indexes.get_index_values(session_date=date.today())
vals_range = kdx.indexes.get_index_values(from_date=start, to_date=end)

### Error Handling

```python
from kythera_kdx import KytheraKdx, KytheraAPIError, KytheraAuthError

kdx = KytheraKdx(x_api_key="xxxx-xxxx-xxxx", client_id="your-client-id", client_secret="your-client-secret", tenant_id="your-tenant-id")

try:
    funds = kdx.funds.get_funds()
    positions = kdx.positions.get_positions()
    pnl = kdx.pnl.get_intraday_pnl_df()
    
    print(f"Successfully retrieved {len(funds)} funds, {len(positions)} positions")
    print(f"Current P&L: {pnl['pnl'].sum():.2f}")
    
except KytheraAuthError:
    print("Authentication failed - check your credentials")
except KytheraAPIError as e:
    print(f"API error: {e.status_code} - {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Available Client Modules

The `KytheraKdx` unified client provides access to specialized modules through properties:

| Module | Access Pattern | Purpose | Key Features |
|--------|----------------|---------|--------------|
| **Funds** | `kdx.funds` | Fund management and NAV data | Fund information, NAV history, fund characteristics |
| **Positions** | `kdx.positions` | Portfolio positions | Current and historical positions, position tracking |
| **Trades** | `kdx.trades` | Trading activity | Trade history, execution data |
| **Instruments** | `kdx.instruments` | Financial instruments | Instrument definitions, characteristics, groups |
| **Prices** | `kdx.prices` | Market pricing | Price data, price types, price overrides |
| **Risk Factors** | `kdx.risk_factors` | Risk management | Risk factor values, risk analytics |
| **P&L** | `kdx.pnl` | Profit & Loss | Intraday P&L, performance analytics |
| **Globals** | `kdx.globals` | Reference data | Calendars, currencies, countries, institutions |
| **Instrument Groups** | `kdx.instrument_groups` | Instrument categorization | Group management and classification |
| **Instrument Parameters** | `kdx.instrument_parameters` | Instrument parameters | Parameter management and configuration |
| **Intraday** | `kdx.intraday` | Real-time data | Intraday market data and analytics |
| **AddIn** | `kdx.addin` | AddIn functionality | Excel AddIn related operations |
| **Issuers** | `kdx.issuers` | Issuer reference data | Issuers list, issuer parameters |

### Example Usage

```python
from kythera_kdx import KytheraKdx

kdx = KytheraKdx(x_api_key="xxxx-xxxx-xxxx", client_id="your-client-id", client_secret="your-client-secret", tenant_id="your-tenant-id")

# All modules are accessible directly from the unified client
funds = kdx.funds.get_funds()
positions = kdx.positions.get_positions()
pnl = kdx.pnl.get_intraday_pnl()
prices = kdx.prices.get_all_prices(date.today(), "CLOSE")
trades = kdx.trades.get_trades(effective_date=date.today())

# Issuers
issuers = kdx.issuers.get_issuers(fetch_characteristics=True)
issuer_params = kdx.issuers.get_issuer_parameters()
```

## Data Models

The library includes comprehensive data models with full type hints:

```python
from kythera_kdx import KytheraKdx
from kythera_kdx.models_v1 import FundDto, PositionDto, TradeDto, PriceDto

kdx = KytheraKdx(x_api_key="xxxx-xxxx-xxxx", client_id="your-client-id", client_secret="your-client-secret", tenant_id="your-tenant-id")

# All responses are automatically parsed into typed objects
funds = kdx.funds.get_funds()
for fund in funds:
    print(f"Fund ID: {fund.id}")
    print(f"Name: {fund.fullName}")
    print(f"Enabled: {fund.isEnabled}")
    print(f"Administrator: {fund.administrator.name}")

# Access positions with full type safety
positions = kdx.positions.get_positions()
for position in positions:
    print(f"Instrument: {position.instrumentName}")
    print(f"Quantity: {position.quantity}")
    print(f"Market Value: {position.marketValue}")
```

## API Compatibility

This library is built against the Kythera Data eXchange API v1 and provides:

- **Full OpenAPI 3.0 Compliance** - Generated from official API specification
- **OAuth2 Security** - Enterprise-grade authentication and authorization
- **RESTful Design** - Standard HTTP methods and status codes
- **JSON Responses** - All data returned in structured JSON format
- **Comprehensive Coverage** - Support for all documented endpoints

## Requirements

- Python 3.7+
- httpx (for HTTP requests)
- pydantic (for data validation and parsing)
- typing-extensions (for enhanced type support)

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/rportela/kythera-api-wrapper.git
cd kythera-api-wrapper

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .
```

### Project Structure

```
kythera-kdx/
├── src/kythera_kdx/          # Main package
│   ├── kythera_kdx.py        # Unified client entry point
│   ├── authenticated_client.py # Core HTTP client with OAuth2
│   ├── funds.py              # Fund management
│   ├── positions.py          # Portfolio positions
│   ├── trades.py             # Trading data
│   ├── prices.py             # Market pricing
│   ├── risk_factors.py       # Risk management
│   ├── pnl.py               # P&L analytics
│   ├── instruments.py        # Financial instruments
│   ├── intraday.py          # Real-time data
│   ├── globals.py           # Reference data
│   ├── models_v1.py         # Data models
│   └── exceptions.py        # Error handling
├── tests/                   # Test suite
├── examples/               # Usage examples
└── docs/                  # Documentation and Jupyter notebooks
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=kythera_kdx --cov-report=html
```

### Code Quality

The project maintains high code quality standards:

```bash
# Code formatting
black src/ tests/

# Import sorting
isort src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Open a Pull Request

## Support and Documentation

- **Examples**: See the `examples/` directory for comprehensive usage examples
- **API Reference**: Generated from OpenAPI specification
- **Issue Tracker**: [GitHub Issues](https://github.com/rportela/kythera-api-wrapper/issues)
- **Changelog**: See [CHANGELOG.md](CHANGELOG.md) for version history

## Why Use the Unified Client?

The `KytheraKdx` unified client provides several advantages:

- **🚀 Single Entry Point**: One client instance gives you access to all Kythera functionality
- **🔧 Simplified Configuration**: Configure authentication once, use everywhere
- **💾 Efficient Resource Usage**: Shared connection pooling and authentication tokens
- **🔒 Consistent Security**: Uniform authentication and error handling across all modules
- **📊 Multiple Data Formats**: Get data as raw JSON, typed objects, or pandas DataFrames
- **🏗️ Lazy Loading**: Client modules are only instantiated when first accessed
- **🎯 IntelliSense Support**: Full IDE support with type hints and autocompletion

### Before (Multiple Clients)
```python
# Old approach - multiple client instances
client = KytheraClient(x_api_key="xxxx-xxxx-xxxx")
funds_client = FundsClient(client)
positions_client = PositionsClient(client)
pnl_client = PnlClient(client)

funds = funds_client.get_funds()
positions = positions_client.get_positions()
pnl = pnl_client.get_intraday_pnl()
```

### After (Unified Client)
```python
# New approach - single unified client
kdx = KytheraKdx(x_api_key="xxxx-xxxx-xxxx")

funds = kdx.funds.get_funds()
positions = kdx.positions.get_positions()
pnl = kdx.pnl.get_intraday_pnl_df()  # Get as DataFrame directly
```

## About Kythera

Kythera is a comprehensive investment management platform that provides:
- Portfolio management and analytics
- Fund administration services  
- Risk management and compliance
- Real-time market data integration
- Comprehensive reporting and analytics

This Python library enables programmatic access to all Kythera platform capabilities through a clean, well-documented API.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
