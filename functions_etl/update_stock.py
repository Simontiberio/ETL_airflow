import pandas as pd
from pathlib import Path

def update_stock(stock_file: str, compras_file: str, ventas_file: str, date: str):

    ''' Update the current stock with the units sold and enters for purchases. Return the updated stock.'''

    # Define directory of files.
    base_dir = './base_datos/inventario'
    base_path = Path(base_dir)
    
    # Load paths.
    stock_path = base_path / stock_file
    compras_path = base_path / compras_file
    ventas_path = base_path / ventas_file
    
    # Verify if all necessary files exist.
    if stock_path.exists() and compras_path.exists() and ventas_path.exists():
        
        # Read stock, purchases, and sales files.
        df_stock = pd.read_excel(stock_path, engine='openpyxl')
        df_compras = pd.read_excel(compras_path, engine='openpyxl')
        df_ventas = pd.read_excel(ventas_path, engine='openpyxl')
        
        # Convert date columns to datetime format.
        df_stock.columns = pd.to_datetime(df_stock.columns, errors='ignore', dayfirst=True)
        df_compras.columns = pd.to_datetime(df_compras.columns, errors='ignore', dayfirst=True)
        df_ventas.columns = pd.to_datetime(df_ventas.columns, errors='ignore', dayfirst=True)
        
        # Convert input date to datetime format.
        date = pd.to_datetime(date, format='%Y-%m-%d')
        
        # If the date doesn't exist in the stock DataFrame, add a new column for it.

        if date not in df_stock.columns:
            
            # Get the most recent stock values (last date).
            last_date = df_stock.columns[-1]
            # Add a new column for the current date, initialized with the stock of the last date.
            df_stock[date] = df_stock[last_date]
        
        # Ensure that the date exists in both the purchases and sales DataFrames.
        if date not in df_compras.columns or date not in df_ventas.columns:
            print(f"Date {date} not found in purchases or sales files.")
            return
        
        # Update stock = stock of the day + units purchased - units sold.
        df_stock[date] = df_stock[date] + df_compras[date] - df_ventas[date]
        
        # Save the updated stock file.
        df_stock.to_excel(stock_path, index=False)
        
        print(f"Stock file has been updated for date {date}.")
    else:
        print("One or more files do not exist. Please check the names and paths.")