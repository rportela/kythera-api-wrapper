# Kythera KDX

A Python wrapper for the Kythera API that provides a simple and intuitive interface for interacting with Kythera services.

## Installation

```bash
pip install kythera-kdx
```

## Quick Start

```python
from kythera_kdx import KytheraClient

# Initialize the client
client = KytheraClient(api_key="your-api-key")

# Make API calls
response = client.get("/endpoint")
print(response)
```

## Features

- 🚀 Simple and intuitive API
- 🔐 Built-in authentication handling
- 🛡️ Comprehensive error handling
- 📝 Full type hints support
- ✅ Extensive test coverage
- 📚 Detailed documentation

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

### Basic GET Request

```python
# Get data from an endpoint
data = client.get("/users")
print(data)
```

### POST Request with Data

```python
# Create a new resource
new_user = {
    "name": "John Doe",
    "email": "john@example.com"
}
response = client.post("/users", data=new_user)
print(f"Created user with ID: {response['id']}")
```

### Error Handling

```python
from kythera_kdx import KytheraClient, KytheraAPIError, KytheraAuthError

client = KytheraClient(api_key="your-api-key")

try:
    response = client.get("/protected-endpoint")
except KytheraAuthError:
    print("Authentication failed - check your API key")
except KytheraAPIError as e:
    print(f"API error: {e.status_code} - {e}")
```

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

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=kythera_kdx --cov-report=html
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
