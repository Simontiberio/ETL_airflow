import pytest
import requests
import pandas as pd
from unittest.mock import patch
from functions_etl.obtain_currency import obtain_currency, append_to_data_price
from utils.config import api_key



# Unit test validates if the dictionary with the expected fields is obtained.

mock_response_api = {
    "rates": {"ARS": 989},
    "date": "2024-10-15"
}

@patch('requests.get')
def test_obtain_currency(mock_get):


    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response_api

    result = obtain_currency(api_key)

    assert result == {'date': '2024-10-15', 'price': 989}, "Result not expected"