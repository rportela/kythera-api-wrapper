from unittest.mock import Mock
import pandas as pd
from datetime import date

from src.kythera_kdx.risk_factors import RiskFactorsClient


def test_get_risk_factor_parameters_and_values():
    mock_client = Mock()

    # parameters
    params_payload = [
        {"name": "RF Param 1", "description": "desc", "parameterType": "STRING"}
    ]
    mock_resp_params = Mock()
    mock_resp_params.json.return_value = params_payload

    # values
    values_payload = [
        {
            "valuationDate": "2025-08-18",
            "riskFactorName": "RF1",
            "riskValueTypeName": "VALUE",
            "value": 0.123,
        }
    ]
    mock_resp_values = Mock()
    mock_resp_values.json.return_value = values_payload

    # get calls should return params first then values
    mock_client.get.side_effect = [mock_resp_params, mock_resp_values]

    client = RiskFactorsClient(mock_client)

    # parameters
    raw_params = client.get_risk_factor_parameters_raw()
    mock_client.get.assert_called_with("/v1/risk-factors/parameters")

    typed_params = client.get_risk_factor_parameters()
    assert typed_params[0].parameterType == "STRING"

    df_params = client.get_risk_factor_parameters_df()
    assert isinstance(df_params, pd.DataFrame)

    # risk factor values
    d = date(2025, 8, 18)
    raw_values = client.get_risk_factor_values_raw(d)
    mock_client.get.assert_called_with("/v1/risk-factor-values", params={"valuation-date": d.isoformat()})

    typed_values = client.get_risk_factor_values(d)
    assert typed_values[0].riskFactorName == "RF1"

    df_values = client.get_risk_factor_values_df(d)
    assert not df_values.empty
