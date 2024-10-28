from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from utils.config import REDSHIFT_HOST,REDSHIFT_DB,REDSHIFT_PORT,REDSHIFT_USER,REDSHIFT_PASSWORD, REDSHIFT_SCHEMA 
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from pathlib import Path
from utils.config import api_key, compras_file,data_quotes,stock_file,ventas_file, list_prices_file,monetized_stock_file


def load_data(file: str):

    '''Reads the file and converts it to parquet format, returning a DataFrame.'''

    # Get extension of the file.
    file_extension = Path(file).suffix.lower()
    
    # Define the path of the file.
    file_path = Path(f"./base_datos/inventario/{file}")

    # Check if the file exists.
    if not file_path.exists():
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")

    # Initialize DataFrame.
    df = None

    # Read files depending on the formats.
    try:
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
            df = df.apply(lambda col: col.astype(str) if col.dtype == 'object' else col)

            # Define parquet file path
            parquet_file_path = file_path.with_suffix('.parquet')
            df.to_parquet(parquet_file_path, engine='pyarrow')
            print("File read as parquet")
            
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path, engine='openpyxl')
            df = df.apply(lambda col: col.astype(str) if col.dtype == 'object' else col)

            # Define parquet file path
            parquet_file_path = file_path.with_suffix('.parquet')
            df.to_parquet(parquet_file_path, engine='pyarrow')
            print("File read as parquet")
        else:
            raise ValueError("File format not supported. Use CSV or XLSX files.")
    
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty. Please provide a valid file with data.")
           
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")

    # Check if the DataFrame was loaded correctly.

    if df is not None:
        return df
    else:
        raise RuntimeError("Failed to load file.")
    
    

def load_data_to_Redshift(file: str):
    
    '''Reads the parquet file, as output of the load_data function, and loads it into the Redshift database.'''

    # Create a dictionary with different tables, and define a table to load in Redshift.
    redshift_tables = {
        stock_file : 'stock_ferrimac',
        ventas_file : 'ventas_unidades',
        list_prices_file : 'list_prices',
        monetized_stock_file: 'stock_monetized',
        data_quotes : 'data_quotes', 
        compras_file : 'compras_stock'
    }

    redshift_table = redshift_tables[file]
   
    # Create URL to connect with SQLAlchemy
    connection_url = f"postgresql://{REDSHIFT_USER}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}"

    # Create connection with SQLAlchemy
    engine = create_engine(connection_url)

    # Establish connection to Redshift
    try:
        with engine.connect() as connection:
            print("Connection to Redshift successful!")
            result = connection.execute("SELECT current_date;")
            for row in result:
                print("Update from Redshift:", row[0])
    except Exception as e:
        raise RuntimeError(f"Error connecting to Redshift: {e}")

    # Load data from parquet file
    df = load_data(file)  # Ensure load_data has error handling
    if df is None:
        raise RuntimeError("DataFrame is empty. Check if the parquet file was loaded correctly.")

    file_stem = Path(file).stem
    file_path = Path(f"./base_datos/inventario/{file_stem}.parquet")
    
    try:
        # Load DataFrame into Redshift table
        df.to_sql(redshift_table, con=engine, schema=REDSHIFT_SCHEMA, if_exists='append', index=False)
        print(f"File loaded into Redshift table '{redshift_table}' successfully.")
    except Exception as e:
        raise RuntimeError(f"Error loading data into Redshift table '{redshift_table}': {e}")