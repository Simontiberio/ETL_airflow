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
    try:
        df_stock['date'] = pd.to_datetime(df_stock['date'], format='%Y-%m-%d', errors='coerce')
        df_compras['date'] = pd.to_datetime(df_compras['date'], format='%Y-%m-%d', errors='coerce')
        df_ventas['date'] = pd.to_datetime(df_ventas['date'], format='%Y-%m-%d', errors='coerce')
        date = pd.to_datetime(date, format='%Y-%m-%d')
        logging.info("Dates converted successfully.")
    except Exception as e:
        logging.error(f"Error converting dates: {e}")
        return

    # Check if a record already exists for the specified date
    if not df_stock[df_stock['date'] == date].empty:
        print(f"A record already exists for {date}. No update was performed.")
        return

    # Filter rows for the specified date in purchases and sales
    compras_dia = df_compras[df_compras['date'] == date]
    ventas_dia = df_ventas[df_ventas['date'] == date]

    # Convert input date to datetime format
    date = pd.to_datetime(date, format='%Y-%m-%d')
    

     # Create a DataFrame with the stock values from the previous day
    stock_day_before = df_stock[df_stock['date'] == (date - pd.Timedelta(days=1))]
    if stock_day_before.empty:
        logging.error("Previous day's stock not found. Please verify the data.")
        return
    else:
        logging.info("Previous day's stock loaded successfully.")

     # Create a new stock record for the current date
    logging.info(f"Creating new stock record for {date}.")
    df_stock_day = stock_day_before.copy()
    df_stock_day['date'] = date
    
    # Update stock by adding purchases and subtracting sales.
    df_stock_day.set_index('id_product', inplace=True)
    compras_dia.set_index('id_product', inplace=True)
    ventas_dia.set_index('id_product', inplace=True)

     # Apply stock update operations
    df_stock_day['Quantity'] += compras_dia['Quantity'].fillna(0) - ventas_dia['Quantity'].fillna(0) 
  
     # Reset index and append the new record
    df_stock_day.reset_index(inplace=True)
    df_stock = pd.concat([df_stock, df_stock_day], ignore_index=True)
    logging.info(f"New stock record created for {date}.")

    # Get the day before the specified date
    yesterday = date - pd.Timedelta(days=1)
    
     
    # Save the updated stock file
    try :
        df_stock.to_excel(stock_path, index=False)
        logging.info(f"Stock file updated for date {date} and saved to {stock_path}.")
    except Exception as e:
        logging.error(f"Error saving stock file: {e}")
                 


