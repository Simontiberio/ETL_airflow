import pandas as pd
from pathlib import Path
import logging
from typing import Union


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_stock(stock_file: str, compras_file: str, ventas_file: str, date: Union[str, pd.Timestamp]):
    """
    Updates the current stock with units sold and purchase entries.
    
    Args:
        stock_file: Name of the stock file.
        compras_file: Name of the purchases file.
        ventas_file: Name of the sales file.
        date: Date for the stock update in 'YYYY-MM-DD' format.
    
    Returns:
         Saves (updated) the updated stock file in the base directory.
    
    Logs:
        Information and errors regarding file existence, date formats, and updates.
    """
    
    # Define the base directory for files
    base_dir = './base_datos/inventario'
    base_path = Path(base_dir)
    
    # Load file paths
    stock_path = base_path / stock_file
    compras_path = base_path / compras_file
    ventas_path = base_path / ventas_file
    
    # Verify if all necessary files exist
    if not all([stock_path.exists(), compras_path.exists(), ventas_path.exists()]):
        logging.error("One or more files do not exist. Please check the names and paths.")
        return
    
    # Read stock, purchases, and sales files
    df_stock = pd.read_excel(stock_path, engine='openpyxl')
    df_compras = pd.read_excel(compras_path, engine='openpyxl')
    df_ventas = pd.read_excel(ventas_path, engine='openpyxl')
    
    # Convert date columns to datetime format
    df_stock.columns = pd.to_datetime(df_stock.columns, format='%Y-%m-%d', errors='ignore', dayfirst=True)
    df_compras.columns = pd.to_datetime(df_compras.columns, format='%Y-%m-%d', errors='ignore', dayfirst=True)
    df_ventas.columns = pd.to_datetime(df_ventas.columns, format='%Y-%m-%d', errors='ignore', dayfirst=True)
    
    # Convert input date to datetime format
    date = pd.to_datetime(date, format='%Y-%m-%d')
    
    # If the date doesn't exist in the stock DataFrame, add a new column for it
    if date not in df_stock.columns:
        last_date = df_stock.columns[-1]
        df_stock[date] = df_stock[last_date]
        logging.info(f"Column for date {date} added with values from the last recorded stock.")
    
    # Ensure that the date exists in both the purchases and sales DataFrames
    if date not in df_compras.columns or date not in df_ventas.columns:
        logging.error(f"Date {date} not found in purchases or sales files.")
        return
    
    # Get the day before the specified date
    yesterday = date - pd.Timedelta(days=1)
    
    # Check if the previous day exists in the stock file
    if yesterday in df_stock.columns:
        # Update stock: stock from the previous day + units purchased - units sold
        df_stock[date] = df_stock[yesterday] + df_compras[date] - df_ventas[date]
        logging.info(f"Stock updated for date {date}.")
    else:
        logging.error(f"The previous date ({yesterday}) does not exist in the stock file.")
        return
    
    # Save the updated stock file
    df_stock.to_excel(stock_path, index=False)
    logging.info(f"Stock file updated for date {date} and saved to {stock_path}.")

                 


