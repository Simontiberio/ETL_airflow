
from functions_etl.load_data import load_data
import pandas as pd
from unittest.mock import patch
import pytest
from pathlib import Path



# Test validates based on the format if it has been loaded correctly

@patch('functions_etl.load_data.Path.exists', return_value=True)
@patch('functions_etl.load_data.pd.read_excel')
@patch('functions_etl.load_data.pd.DataFrame.to_parquet')
def test_load_data_xlsx(mock_to_parquet, mock_read_excel, mock_exists):
    # Mock DataFrame to return.
    mock_df = pd.DataFrame({'colA': ['1', '2'], 'colB': ['3', '4']})
    mock_read_excel.return_value = mock_df
    
    # Execute function.
    result = load_data('test_file.xlsx')
    
    # Check if 'read_excel' is read correctly.
    mock_read_excel.assert_called_once_with(Path('./base_datos/inventario/test_file.xlsx'), engine='openpyxl')
    
    # Check if DF is become as parquet file.
    mock_to_parquet.assert_called_once()

        
    # Checl result expected.
    pd.testing.assert_frame_equal(result, mock_df)

    # Check the path where new file load.
    expected_parquet_path = Path('./base_datos/inventario/test_file.parquet')

    result_return = mock_to_parquet.call_args[0][0]


    assert result_return == expected_parquet_path