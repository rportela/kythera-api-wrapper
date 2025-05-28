"""
Basic tests for the KytheraClient class.
"""

import pytest
import requests_mock
from kythera_kdx import KytheraClient
from kythera_kdx.exceptions import KytheraAPIError, KytheraAuthError


class TestKytheraClient:
    """Test cases for the KytheraClient class."""
    
    def test_client_initialization(self):
        """Test client initialization with default parameters."""
        client = KytheraClient()
        assert client.base_url == "https://api.kythera.com"
        assert client.timeout == 30
        assert client.api_key is None
    
    def test_client_initialization_with_params(self):
        """Test client initialization with custom parameters."""
        client = KytheraClient(
            base_url="https://custom.api.com",
            api_key="test-key",
            timeout=60
        )
        assert client.base_url == "https://custom.api.com"
        assert client.api_key == "test-key"
        assert client.timeout == 60
        assert "Bearer test-key" in client.session.headers["Authorization"]
    
    @requests_mock.Mocker()
    def test_successful_get_request(self, m):
        """Test successful GET request."""
        client = KytheraClient(api_key="test-key")
        mock_response = {"status": "success", "data": []}
        
        m.get("https://api.kythera.com/test", json=mock_response)
        
        response = client.get("/test")
        assert response == mock_response
    
    @requests_mock.Mocker()
    def test_successful_post_request(self, m):
        """Test successful POST request."""
        client = KytheraClient(api_key="test-key")
        mock_response = {"status": "created", "id": 123}
        request_data = {"name": "test"}
        
        m.post("https://api.kythera.com/test", json=mock_response)
        
        response = client.post("/test", data=request_data)
        assert response == mock_response
    
    @requests_mock.Mocker()
    def test_api_error_handling(self, m):
        """Test API error handling."""
        client = KytheraClient(api_key="test-key")
        
        m.get("https://api.kythera.com/test", status_code=400, json={"error": "Bad request"})
        
        with pytest.raises(KytheraAPIError) as exc_info:
            client.get("/test")
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.response_data == {"error": "Bad request"}
    
    @requests_mock.Mocker()
    def test_auth_error_handling(self, m):
        """Test authentication error handling."""
        client = KytheraClient(api_key="invalid-key")
        
        m.get("https://api.kythera.com/test", status_code=401)
        
        with pytest.raises(KytheraAuthError):
            client.get("/test")
    
    def test_set_api_key(self):
        """Test setting API key after initialization."""
        client = KytheraClient()
        assert client.api_key is None
        
        client.set_api_key("new-key")
        assert client.api_key == "new-key"
        assert "Bearer new-key" in client.session.headers["Authorization"]
