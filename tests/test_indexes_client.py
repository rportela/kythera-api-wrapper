from unittest.mock import Mock
import pandas as pd
from datetime import date

from src.kythera_kdx.indexes import IndexesClient


def test_get_index_values_query_params_and_shapes():
    mock_client = Mock()
    sample = [
        {"indexName": "IDX1", "sessionDate": "2025-08-18", "value": 123.45},
        {"indexName": "IDX2", "sessionDate": "2025-08-18", "value": 67.89},
    ]
    mock_resp = Mock()
    mock_resp.json.return_value = sample
    mock_client.get.return_value = mock_resp

    client = IndexesClient(mock_client)

    # session-date
    d = date(2025, 8, 18)
    raw = client.get_index_values_raw(session_date=d)
    mock_client.get.assert_called_with(
        "/v1/indexes/values", params={"session-date": d.isoformat()}
    )
    assert isinstance(raw, list) and len(raw) == 2

    typed = client.get_index_values(session_date=d)
    assert typed[0].indexName == "IDX1"

    df = client.get_index_values_df(session_date=d)
    assert isinstance(df, pd.DataFrame) and df.shape[0] == 2

    # from-date/to-date
    mock_client.get.reset_mock()
    start = date(2025, 8, 1)
    end = date(2025, 8, 18)
    client.get_index_values_raw(from_date=start, to_date=end)
    mock_client.get.assert_called_with(
        "/v1/indexes/values",
        params={"from-date": start.isoformat(), "to-date": end.isoformat()},
    )
