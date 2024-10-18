import requests
import os
import pandas as pd
from utils.config import api_key, data_quotes
from pathlib import Path




def obtain_currency(api_key):

    '''Function that allows us to obtain the dollar price, returning a dictionary with the rate and its date'''


    url = "https://api.apilayer.com/exchangerates_data/latest"
    
    params = { "symbols": "ARS",  
        "base": "USD" }
    headers = {
        "apikey": api_key}
    response = requests.get(url, headers=headers, params=params)
    # Check the result of response, if some failure exist.
    if response.status_code == 200:
        data = response.json()
        cotizacion_dolar = data['rates']['ARS']
        print(f"Current dolar rates: {cotizacion_dolar} ARS")
        registro = { 'date': data['date'] , 'price': data['rates']['ARS']}
        return registro
    else:
        print(f"Error getting price: {response.status_code}, {response.text}")




def append_to_data_price(api_key : str, data_quotes : str):
    
    ''' Get the current record of the dollar price. To then host it as a dictionary, 
    for example: {'date': '2024-mm-dd', 'price': 965}. '''

    record = obtain_currency(api_key) 
    print(record)

   
    #base_dir = './base_datos/inventario/'
    #base_path = Path(base_dir)
    file_path = f"./base_datos/inventario/{data_quotes}"

    # Check if the price file already exists, if not, create an empty DataFrame with the appropriate columns,
    #and then enter the values extracted by the API.
    
    if os.path.exists(file_path):
        data_prices = pd.read_csv(file_path)
    else:
        data_prices = pd.DataFrame(columns=['date', 'price'])

    # Check if the day's record is already in the DataFrame, to avoid duplicating records.
    
    if record['date'] in data_prices['date'].values:
        print(f"Record of day {record['date']} just exist. Not add again.")
        return data_prices

    # Convert the record to a DataFrame and add it to data_prices(file).
    
    new_record = pd.DataFrame([record])
    data_prices = pd.concat([data_prices, new_record], ignore_index=True)

    #Save the updated DataFrame to the CSV file.
    
    data_prices.to_csv(file_path, index=False)
    print(f"Record of day {record['date']} added successfully.")
    
    return data_prices