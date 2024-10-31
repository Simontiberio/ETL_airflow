import requests
import os
import pandas as pd
from etl_airflow.config import api_key




# Function that allows us to obtain the dollar price, returning a dictionary with the rate and its date

def obtain_currency(api_key):
    url = "https://api.apilayer.com/exchangerates_data/latest"
    params = { "symbols": "ARS",  
        "base": "USD" }
    headers = {
        "apikey": api_key}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        cotizacion_dolar = data['rates']['ARS']
        print(f"Cotización actual del dólar: {cotizacion_dolar} ARS")
        registro = { 'date': data['date'] , 'price': data['rates']['ARS']}
        return registro
    else:
        print(f"Error al obtener la cotización: {response.status_code}, {response.text}")



def append_to_data_price( path : str ):
    #Save price of dollar in a variable.

    registro = obtain_currency(api_key)

    # Check if prices file (DF) exist, if not create one.
    if os.path.exists(path):
        data_prices = pd.read_csv(path)
    else:
        data_prices = pd.DataFrame(columns=['date', 'price'])

    # Convert the dictionary into a df, and add it to the prices df
        
    nuevo_registro = pd.DataFrame([registro])
    data_prices = pd.concat([data_prices, nuevo_registro], ignore_index=True)

    # Save and up date prices df.    
    data_prices.to_csv(path, index=False)
    
    return data_prices