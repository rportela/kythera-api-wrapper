#!/usr/bin/env python3
"""
Test script to verify the revised PnlClient implementation.
"""

from src.kythera_kdx.pnl import PnlClient
from src.kythera_kdx.models_v1 import IntradayPnlEntryDto
from unittest.mock import Mock
import pandas as pd
import math


def test_pnl_client():
    """Test the PnlClient implementation."""
    
    # Mock the authenticated client
    mock_client = Mock()
    
    # Mock response data - sample IntradayPnlEntryDto data
    sample_data = [
        {
            "pnl": 1000.50,
            "pnlTrade": 500.25,
            "pnlPosition": 500.25,
            "instrumentName": "TEST_INSTRUMENT_1",
            "fundName": "TEST_FUND_1",
            "portfolioName": "TEST_PORTFOLIO_1"
        },
        {
            "pnl": -250.75,
            "pnlTrade": -125.30,
            "pnlPosition": -125.45,
            "instrumentName": "TEST_INSTRUMENT_2",
            "fundName": "TEST_FUND_2", 
            "portfolioName": "TEST_PORTFOLIO_2"
        }
    ]
    
    # Mock the response
    mock_response = Mock()
    mock_response.json.return_value = sample_data
    mock_client.get.return_value = mock_response
    
    # Create PnlClient instance
    pnl_client = PnlClient(mock_client)
    
    print("Testing PnlClient implementation...")
    
    # Test 1: get_intraday_pnl_raw()
    print("\n1. Testing get_intraday_pnl_raw()...")
    raw_data = pnl_client.get_intraday_pnl_raw()
    assert isinstance(raw_data, list)
    assert len(raw_data) == 2
    assert math.isclose(raw_data[0]["pnl"], 1000.50, rel_tol=1e-9)
    print("   ✓ Raw data method works correctly")
    
    # Test 2: get_intraday_pnl() 
    print("\n2. Testing get_intraday_pnl()...")
    typed_data = pnl_client.get_intraday_pnl()
    assert isinstance(typed_data, list)
    assert len(typed_data) == 2
    assert isinstance(typed_data[0], IntradayPnlEntryDto)
    assert math.isclose(typed_data[0].pnl or 0.0, 1000.50, rel_tol=1e-9)
    assert math.isclose(typed_data[1].pnl or 0.0, -250.75, rel_tol=1e-9)
    print("   ✓ Typed data method works correctly")
    
    # Test 3: get_intraday_pnl_df()
    print("\n3. Testing get_intraday_pnl_df()...")
    df = pnl_client.get_intraday_pnl_df()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert math.isclose(float(df.iloc[0]["pnl"]), 1000.50, rel_tol=1e-9)
    assert math.isclose(float(df.iloc[1]["pnl"]), -250.75, rel_tol=1e-9)
    print("   ✓ DataFrame method works correctly")
    
    # Verify proper client method calls
    assert mock_client.get.call_count == 3  # Called once for each method
    mock_client.get.assert_called_with("/v1/pnl/intraday")
    
    print("\n✅ All tests passed! PnlClient implementation is correct.")
    print(f"   - Raw method returns: {type(raw_data)} with {len(raw_data)} items")
    print(f"   - Typed method returns: {type(typed_data)} with {len(typed_data)} IntradayPnlEntryDto objects")
    print(f"   - DataFrame method returns: {type(df)} with shape {df.shape}")


def test_pnl_explain_params_and_shapes():
    from datetime import date
    mock_client = Mock()

    payload = [
        {"id": 1, "pnl": 10.5, "explainDetails": {"fundName": "F1"}},
        {"id": 2, "pnl": -2.0, "explainDetails": {"fundName": "F2"}},
    ]
    mock_resp = Mock()
    mock_resp.json.return_value = payload
    mock_client.get.return_value = mock_resp

    pnl_client = PnlClient(mock_client)

    start = date(2025, 8, 1)
    end = date(2025, 8, 19)
    disc = ["fundName", "instrumentName"]

    raw = pnl_client.get_pnl_explain_raw(start, end, "MASTER", disc)
    assert isinstance(raw, list) and len(raw) == 2

    # Verify query param shapes (array as repeated key encoded via list)
    mock_client.get.assert_called_with(
        "/v1/pnl/explain",
        params={
            "start-date": start.isoformat(),
            "end-date": end.isoformat(),
            "fund-family": "MASTER",
            "discriminator": disc,
        },
    )

    typed = pnl_client.get_pnl_explain(start, end, "MASTER", disc)
    assert hasattr(typed[0], "pnl")

    df = pnl_client.get_pnl_explain_df(start, end, "MASTER", disc)
    assert not df.empty


if __name__ == "__main__":
    test_pnl_client()
    test_pnl_explain_params_and_shapes()
