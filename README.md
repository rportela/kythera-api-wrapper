# Kythera KDX

A Python wrapper for the Kythera Data eXchange (KDX) API that provides a comprehensive interface for accessing financial and investment management data. This library enables portfolio managers, fund administrators, and financial professionals to programmatically interact with Kythera's investment management platform.

## Installation

```bash
pip install kythera-kdx     
```

## Quick Start

```python
from kythera_kdx import KytheraClient, FundsClient, PositionsClient

# Initialize the client
client = KytheraClient(api_key="your-api-key")

# Get fund information
funds_client = FundsClient(client)
funds = funds_client.get_funds(enabled_only=True)

# Get positions for today
positions_client = PositionsClient(client)
positions = positions_client.get_positions(is_open=True)

print(f"Found {len(funds)} funds and {len(positions)} positions")
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

## Configuration

### Environment Variables

You can set your API key using environment variables:

```bash
export KYTHERA_API_KEY="your-api-key"
```

### Client Configuration

```python
from kythera_kdx import KytheraClient

# Basic configuration
client = KytheraClient(
    api_key="your-api-key",
    base_url="https://api.kythera.com",  # Optional, uses default
    timeout=30  # Optional, request timeout in seconds
)
```

## Usage Examples

### Working with Funds

```python
from kythera_kdx import KytheraClient, FundsClient
from datetime import date

client = KytheraClient(api_key="your-api-key")
funds_client = FundsClient(client)

# Get all enabled funds with characteristics
funds = funds_client.get_funds(enabled_only=True, fetch_characteristics=True)
for fund in funds:
    print(f"Fund: {fund.fullName} ({fund.shortName})")

# Get fund NAVs for a specific date
navs = funds_client.get_fund_navs(date=date.today())
for nav in navs:
    print(f"Fund {nav.fundName}: {nav.value} on {nav.date}")
```

### Portfolio Positions

```python
from kythera_kdx import PositionsClient
from datetime import date

positions_client = PositionsClient(client)

# Get current open positions
positions = positions_client.get_positions(is_open=True)
for position in positions:
    print(f"Position: {position.instrumentName} - Quantity: {position.quantity}")

# Get positions for a specific date
historical_positions = positions_client.get_positions(
    position_date=date(2024, 1, 15),
    is_open=False
)
```

### Trading Data

```python
from kythera_kdx import TradesClient
from datetime import date

trades_client = TradesClient(client)

# Get trades for today
trades = trades_client.get_trades(effective_date=date.today())
for trade in trades:
    print(f"Trade: {trade.instrumentName} - {trade.quantity} @ {trade.price}")
```

### Market Prices and Risk Data

```python
from kythera_kdx import PricesClient, RiskFactorsClient
from datetime import date

# Get pricing data
prices_client = PricesClient(client)
prices = prices_client.get_all_prices(
    price_date=date.today(),
    price_type_name="CLOSE"
)

# Get risk factor values
risk_client = RiskFactorsClient(client)
risk_factors = risk_client.get_risk_factor_values(valuation_date=date.today())
```

### P&L Analysis

```python
from kythera_kdx import PnlClient

pnl_client = PnlClient(client)

# Get current intraday P&L
intraday_pnl = pnl_client.get_intraday_pnl()
print(f"Intraday P&L: {intraday_pnl}")
```

### Error Handling

```python
from kythera_kdx import KytheraClient, KytheraAPIError, KytheraAuthError

client = KytheraClient(api_key="your-api-key")
funds_client = FundsClient(client)

try:
    funds = funds_client.get_funds()
except KytheraAuthError:
    print("Authentication failed - check your API key")
except KytheraAPIError as e:
    print(f"API error: {e.status_code} - {e}")
```

## Available Client Modules

The library provides specialized client modules for different aspects of the Kythera platform:

| Module | Purpose | Key Features |
|--------|---------|--------------|
| **FundsClient** | Fund management and NAV data | Fund information, NAV history, fund characteristics |
| **PositionsClient** | Portfolio positions | Current and historical positions, position tracking |
| **TradesClient** | Trading activity | Trade history, execution data |
| **InstrumentsClient** | Financial instruments | Instrument definitions, characteristics, groups |
| **PricesClient** | Market pricing | Price data, price types, price overrides |
| **RiskFactorsClient** | Risk management | Risk factor values, risk analytics |
| **PnlClient** | Profit & Loss | Intraday P&L, performance analytics |
| **GlobalsClient** | Reference data | Calendars, currencies, countries, institutions |
| **InstrumentGroupsClient** | Instrument categorization | Group management and classification |
| **InstrumentParametersClient** | Instrument parameters | Parameter management and configuration |
| **IntradayClient** | Real-time data | Intraday market data and analytics |

## Data Models

The library includes comprehensive data models with full type hints:

```python
from kythera_kdx.models_v1 import FundDto, PositionDto, TradeDto, PriceDto

# All responses are automatically parsed into typed objects
funds = funds_client.get_funds()
for fund in funds:
    print(f"Fund ID: {fund.id}")
    print(f"Name: {fund.fullName}")
    print(f"Enabled: {fund.isEnabled}")    print(f"Administrator: {fund.administrator.name}")
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
│   ├── client.py             # Core HTTP client
│   ├── funds.py              # Fund management
│   ├── positions.py          # Portfolio positions
│   ├── trades.py             # Trading data
│   ├── prices.py             # Market pricing
│   ├── risk_factors.py       # Risk management
│   ├── pnl.py               # P&L analytics
│   ├── instruments.py        # Financial instruments
│   ├── globals.py           # Reference data
│   ├── models_v1.py         # Data models
│   └── exceptions.py        # Error handling
├── tests/                   # Test suite
├── examples/               # Usage examples
└── docs/                  # Documentation
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
