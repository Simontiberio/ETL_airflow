import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env

DIR_PATH: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path: str = os.path.join(DIR_PATH, '.env')
load_dotenv(dotenv_path)


# Acceder a las variables de entorno

AIRFLOW_UID=os.environ.get('AIRFLOW_UID')


REDSHIFT_USER = os.environ.get('REDSHIFT_USER')
REDSHIFT_PASSWORD = os.environ.get('REDSHIFT_PASSWORD')
REDSHIFT_DB = os.environ.get('REDSHIFT_DB')
REDSHIFT_HOST = os.environ.get('REDSHIFT_HOST')
REDSHIFT_PORT = os.environ.get('REDSHIFT_PORT')
REDSHIFT_SCHEMA = os.environ.get('REDSHIFT_SCHEMA')

api_key = os.environ.get('api_key')

compras_file = os.environ.get('compras_file')
ventas_file = os.environ.get ('ventas_file')
stock_file = os.environ.get ('stock_file')
data_quotes = os.environ.get ('data_quotes')
monetized_stock_file = os.environ.get ('monetized_stock_file')
list_prices_file = os.environ.get ('list_prices_file')

