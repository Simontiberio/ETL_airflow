import pandas as pd
from pathlib import Path
from utils.config import list_prices_file, monetized_stock_file
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monetize_stock (stock_file: str, data_quotes: str, date: str):

    """
    Calculates the value of the product stock in local currency based on daily stock, price list, and exchange rates.
    
    Args:
        stock_file (str): Name of the stock file in Excel format.
        data_quotes (str): Name of the exchange rate file in CSV format.
        date (str): Date for which the stock will be monetized, in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame or None: DataFrame with monetized stock if successful, otherwise None.
        
    Logs:
        - Errors if required files are missing or if the specified date is not found.
        - Warnings if the price for the date is missing in the quotes data.
        - Information on successful updates to the stock file.
    """
    
    # Define directory of files.
    
    base_dir = './base_datos/inventario'
    base_path = Path(base_dir)
    
    
    # Load paths.
    stock_path = base_path / stock_file
    list_prices_path = base_path / list_prices_file
    quotes_path = base_path / data_quotes
    monetized_stock_path = base_path / monetized_stock_file
    
    # Verify if all necessary files exist.
    if not (stock_path.exists() and list_prices_path.exists() and quotes_path.exists()):
        logging.error("One or more files do not exist. Check the names and paths.")
        return None

    # Read stock, list price and quotes files.
    df_stock = pd.read_excel(stock_path, engine='openpyxl')
    df_quotes = pd.read_csv(quotes_path)
    df_list_prices = pd.read_excel(list_prices_path, engine='openpyxl')
        
    # Convert date columns to datetime format.
    df_stock['date']  = pd.to_datetime(df_stock['date'], dayfirst=True, format='%Y-%m-%d')
    df_quotes['date'] = pd.to_datetime(df_quotes['date'], errors='coerce', format='%Y-%m-%d')
    df_list_prices['date'] = pd.to_datetime(df_list_prices['date'], format='%Y-%m-%d', dayfirst=True)
        
    # Convert date to datetime format. 
    date = pd.to_datetime(date, format='%Y-%m-%d')

    # Create a new DF to calculate stock valuation of the day.

    df = df_stock[df_stock['date'] == date ]
    df.loc [:,'date'] = date
        
    # Check if the date exists in df_quotes.
    if date not in df_quotes['date'].values:
        logging.warning(f"Date {date} not found in the quotes file.")
        return None
            
    current_price = df_quotes.loc[df_quotes['date'] == date, 'price'].values
    if not current_price:
        logging.warning(f"Price not found for date {date}.")
        return None
    
    # Get the first value of the price.
    current_price = current_price[0]  

    #Get the latest list of price.
    last_date = df_list_prices['date'].max()
    latest_prices = df_list_prices[df_list_prices['date'] == last_date]
    latest_prices = latest_prices['price'].round(2)
                
    # Calculate the stock monetized by the price and list prices for the given date.
    df_amount = latest_prices * current_price * df['Quantity'].values
    df['Quantity'] = df_amount.values.round(2)
    df = df.rename(columns={'Quantity': 'amount'})

    # Load the existing monetized stock file if it exists.
    if monetized_stock_path.exists():
        df_monetized_stock = pd.read_excel(monetized_stock_path, engine='openpyxl')
        df_monetized_stock['date'] = pd.to_datetime(df_monetized_stock['date'], errors='coerce', format='%Y-%m-%d')
    
    # Update the current date in df_monetized_stock.

    if date in df_monetized_stock['date'].values:
       logging.info(f"Data is already found for {date}. Please check what is uploaded.")
    else:
     # Update only the rows that correspond to existing products
        df_monetized_stock = pd.concat([df_monetized_stock, df], ignore_index=True)

        # Save the updated stock with all dates to the file.
        df_monetized_stock.to_excel(monetized_stock_path, index=False)

     # Convert the DataFrame as a Parquet file
    parquet_path = monetized_stock_path.with_suffix('.parquet')
    df_monetized_stock['model'] = df_monetized_stock['model'].astype(str)
    df_monetized_stock.to_parquet(parquet_path, index=False, engine='pyarrow')
                
    logging.info(f"Monetized stock has been successfully updated for date {date}.")
    return df_monetized_stock            