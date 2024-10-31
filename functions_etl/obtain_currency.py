import requests
import os
import pandas as pd
from utils.config import api_key, data_quotes
from pathlib import Path
import logging
from datetime import datetime



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def obtain_currency(api_key):

    """
    Fetches the current USD to ARS exchange rate, returning a dictionary with the rate and date.
    
    Args:
        api_key: API key for authenticating the request to the exchange rate service.
    
    Returns:
        Dictionary containing the date and exchange rate if successful, or None on failure.
    
    Logs:
        - Information about the current dollar rate if the request is successful.
        - Error details if the request fails.
    """


    url = "https://api.apilayer.com/currency_data/live?source=USD&currencies=ARS"
    
    headers = {
        "apikey": api_key
    }
        
    response = requests.get(url, headers=headers)
    # Check the result of response, if some failure exist.
    if response.status_code == 200:
        data = response.json()
        current_dollar = data['quotes']['USDARS']
        logging.info(f"Current dollar rate: {current_dollar} ARS")

        date_today = datetime.now().strftime('%Y-%m-%d')

        record = { 'date': date_today , 'price': current_dollar}
        logging.info(f"Current dollar rate: {current_dollar} ARS on {date_today}")
        return record
    
    else:
        logging.error(f"Error getting price: {response.status_code}, {response.text}")




def append_to_data_price(api_key : str, data_quotes : str):
    
    """
    Retrieves the current dollar price record from an API and appends it to a CSV file. 
    The record is structured as a dictionary.
    
    Args:
        api_key: API key used to authenticate and obtain currency data.
        data_quotes: Name of the CSV file where data is stored.
        
    Returns:
        DataFrame: Updated DataFrame containing all records, including the newly appended one if applicable.
        
    Logs:
        - Information about existing records.
        - Successful addition of a new record.
        - Errors if the record for the current date already exists.
    """

    record = obtain_currency(api_key) 
    logging.info(f"Obtained record: {record}")

      
    file_path = f"./base_datos/inventario/{data_quotes}"

    # Check if the price file already exists, if not, create an empty DataFrame with the appropriate columns,
    #and then enter the values extracted by the API.
    
    if os.path.exists(file_path):
        data_prices = pd.read_csv(file_path)
    else:
        data_prices = pd.DataFrame(columns=['date', 'price'])
        logging.info(f"Created new file for {data_quotes} with columns 'date' and 'price'.")

    # Check if the day's record is already in the DataFrame, to avoid duplicating records.
    
    if record['date'] in data_prices['date'].values:
        logging.warning(f"Record for {record['date']} already exists. No new entry added.")
        return data_prices

    # Convert the record to a DataFrame and add it to data_prices(file).
    
    new_record = pd.DataFrame([record])
    data_prices = pd.concat([data_prices, new_record], ignore_index=True)

    #Save the updated DataFrame to the CSV file.
    
    data_prices.to_csv(file_path, index=False)
    logging.info(f"Record for {record['date']} added successfully to {data_quotes}.")
    
    return data_prices