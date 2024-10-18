
from functions_etl.load_data import load_data
import pandas as pd
from unittest.mock import patch
import pytest



# Test validates based on the format if it has been loaded correctly

@patch('functions_etl.load_data.Path.exists', return_value=True)
@patch('functions_etl.load_data.pd.read_excel')
@patch('functions_etl.load_data.pd.DataFrame.to_parquet')
def test_load_data_xlsx(mock_to_parquet, mock_read_excel, mock_exists):

    
    mock_df = pd.DataFrame({'col1': ['1', '2'], 'col2': ['3', '4']})
    mock_read_excel.return_value = mock_df
    
    result = load_data('test_file.xlsx')