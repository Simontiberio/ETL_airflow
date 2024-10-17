import pandas as pd
from pathlib import Path
from utils.config import list_prices_file, monetized_stock_file



import pandas as pd
from pathlib import Path

def monetize_stock (stock_file: str, data_quotes: str, date: str):
    # Define directory of files.
    
    base_dir = './base_datos/inventario'
    base_path = Path(base_dir)
    
    
    # Load paths.
    stock_path = base_path / stock_file
    list_prices_path = base_path / list_prices_file
    quotes_path = base_path / data_quotes
    monetized_stock_path = base_path / monetized_stock_file
    
    # Verify if all necessary files exist.
    if stock_path.exists() and list_prices_path.exists() and quotes_path.exists():
        # Read stock, list price and quotes files.
        df_stock = pd.read_excel(stock_path, engine='openpyxl')
        df_quotes = pd.read_csv(quotes_path)
        df_list_prices = pd.read_excel(list_prices_path, engine='openpyxl')
        
        # Convert date columns to datetime format.
        df_stock.columns = pd.to_datetime(df_stock.columns, errors='ignore', dayfirst=True)
        df_quotes['date'] = pd.to_datetime(df_quotes['date'], errors='coerce', format='%Y-%m-%d')
        df_list_prices.columns = pd.to_datetime(df_list_prices.columns, errors='ignore', dayfirst=True)
        
        # Convert date to datetime format. 
        date = pd.to_datetime(date, format='%Y-%m-%d')
        
        # Check if the date exists in df_quotes.
        if date in df_quotes['date'].values:
            current_price = df_quotes.loc[df_quotes['date'] == date, 'price'].values
            if len(current_price) > 0:
                current_price = current_price[0]  # Get the first value of the price.

                # Create DataFrame with the current prices so that the arithmetic calculation can be done.
                current_price_df = pd.DataFrame({'price': [current_price] * len(df_stock['id_product'])})
                
                # Calculate the stock monetized by the price and list prices for the given date.
                monetized_values = (df_stock[date] * current_price_df['price'] * df_list_prices.iloc[:, -1]).round(2)

                # Load the existing monetized stock file if it exists.
                if monetized_stock_path.exists():
                    df_monetized_stock = pd.read_excel(monetized_stock_path, engine='openpyxl')
                else:
                    df_monetized_stock = pd.DataFrame({'id_product': df_stock['id_product']})

                # Update or create the column for the current date in df_monetized_stock.
                if date not in df_monetized_stock.columns:
                    df_monetized_stock[date] = monetized_values
                else:
                    # Update only the rows that correspond to existing products
                    df_monetized_stock[date].update(monetized_values)

                # Save the updated stock with all dates to the file.
                df_monetized_stock.to_excel(monetized_stock_path, index=False)
                
                print(f"Stock file has been updated for date {date}.")
            else:
                print(f"Price not found for date {date}.")
        else:
            print(f"Date {date} not found in df_quotes['date'].")
    else:
        print("One or more files do not exist. Check the names and paths.")

