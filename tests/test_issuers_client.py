from unittest.mock import Mock
import pandas as pd

from src.kythera_kdx.issuers import IssuersClient


def test_get_issuers_endpoints_and_params():
    mock_client = Mock()
    sample = [
        {
            "name": "Issuer A",
            "description": "Desc A",
            "tinNumber": "A123",
            "issuerCountryName": "BR",
            "parentIssuerName": "Parent A",
        },
        {
            "name": "Issuer B",
            "description": "Desc B",
            "tinNumber": "B456",
            "issuerCountryName": "US",
            "parentIssuerName": "Parent B",
        },
    ]
    mock_resp = Mock()
    mock_resp.json.return_value = sample
    mock_client.get.return_value = mock_resp

    client = IssuersClient(mock_client)

    # Default: fetchCharacteristics False
    raw = client.get_issuers_raw()
    mock_client.get.assert_called_with("/v1/issuers", params={"fetchCharacteristics": False})
    assert isinstance(raw, list) and len(raw) == 2

    # Typed
    typed = client.get_issuers()
    assert typed[0].name == "Issuer A"

    # DataFrame
    df = client.get_issuers_df()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2

    # With fetchCharacteristics True
    client.get_issuers_raw(True)
    mock_client.get.assert_called_with("/v1/issuers", params={"fetchCharacteristics": True})


def test_get_issuer_parameters():
    mock_client = Mock()
    sample_params = [
        {
            "name": "Issuer A",
            "description": "Desc A",
            "tinNumber": "A123",
            "issuerCountryName": "BR",
            "parentIssuerName": "Parent A",
        }
    ]
    mock_resp = Mock()
    mock_resp.json.return_value = sample_params
    mock_client.get.return_value = mock_resp

    client = IssuersClient(mock_client)

    raw = client.get_issuer_parameters_raw()
    mock_client.get.assert_called_with("/v1/issuers/parameters")
    assert isinstance(raw, list) and len(raw) == 1

    typed = client.get_issuer_parameters()
    assert typed[0].tinNumber == "A123"

    df = client.get_issuer_parameters_df()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
