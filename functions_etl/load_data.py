from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from utils.config import REDSHIFT_HOST,REDSHIFT_DB,REDSHIFT_PORT,REDSHIFT_USER,REDSHIFT_PASSWORD 
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


# Create URL to connect with SQLAlchemy
connection_url = f"postgresql://{REDSHIFT_USER}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}"

# Create connection with SQLAlchemy
engine = create_engine(connection_url)

try:
    with engine.connect() as connection:
        print("Connection to Redshift successful!")
        result = connection.execute("SELECT current_date;")
        for row in result:
            print("update from Redshift:", row[0])
except Exception as e:
    print(f"Error getting with Redshift conection: {e}")


df_price = pd.read_csv('base_datos/data_price.csv')
df_price.to_sql(name='data_prices', con=engine, schema='2024_simon_tiberio_schema', if_exists='append', index=False)