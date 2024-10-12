import pandas as pd
from pathlib import Path

def update_stock(stock_file: str, compras_file: str, ventas_file: str, date: str):
    # Define directory of files.
    base_dir = './base_datos/inventario'
    base_path = Path(base_dir)
    
    # Load files.
    stock_path = base_path / stock_file
    compras_path = base_path / compras_file
    ventas_path = base_path / ventas_file
    
    if stock_path.exists() and compras_path.exists() and ventas_path.exists():
        # Rad stock, purchases and sells files.


        df_stock = pd.read_excel(stock_path, engine='openpyxl')
        df_compras = pd.read_excel(compras_path, engine='openpyxl')
        df_ventas = pd.read_excel(ventas_path, engine='openpyxl')
        
        
       # Convert date columns to datetime format, then match the formats.


        df_stock.columns = pd.to_datetime(df_stock.columns, errors='ignore', dayfirst=True)
        df_compras.columns = pd.to_datetime(df_compras.columns, errors='ignore', dayfirst=True)
        df_ventas.columns = pd.to_datetime(df_ventas.columns, errors='ignore', dayfirst=True)
        
        # Convert date ti datetime format.
        date = pd.to_datetime(date, format='%Y-%m-%d')

        
        # Check if a date is in a columns of DF.
        if date not in df_stock.columns or date not in df_compras.columns or date not in df_ventas.columns:
            print(f" Date {date} is not in file.{df_stock.columns}")
            return
        
        # Get the column from the day before the last one, this case would be viable if the update of the files we use is done automatically. 
        # As in real life.
        #previous_date = df_stock.columns[-1]
        
        # Update stock = stock of day + units purchases - units sells.
        df_stock[date] = df_stock[date] + df_compras[date] - df_ventas[date]
        
        # Save a updated file.
        df_stock.to_excel(stock_path, index=False)
        
        print(f"Stock file has been updated for date {date}.")
    else:
        print("One or more files do not exist. Please check the names and paths.")