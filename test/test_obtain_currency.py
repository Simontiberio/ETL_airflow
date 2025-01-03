import pytest
import requests
import pandas as pd
from unittest.mock import patch
from functions_etl.obtain_currency import obtain_currency
from utils.config import api_key
from datetime import datetime



# Unit test validates if the dictionary with the expected fields is obtained.

mock_response_api = {
    "quotes": {"USDARS": 989},
    "date": "2024-10-15"
}

@patch('requests.get')
def test_obtain_currency(mock_get):

    """
    Tests the obtain_currency function to ensure it retrieves and returns 
    the correct currency data from an external API.

    Args:
        mock_get (MagicMock): Mock of the requests.get function to simulate the 
                              API call and return a pre-defined JSON response.
    """


    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response_api

    result = obtain_currency(api_key)

    expected_date = datetime.now().strftime('%Y-%m-%d')
    expected = {'date': expected_date, 'price': 989}

    assert result == expected , "Result not expected"