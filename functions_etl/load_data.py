from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from utils.config import REDSHIFT_HOST,REDSHIFT_DB,REDSHIFT_PORT,REDSHIFT_USER,REDSHIFT_PASSWORD, REDSHIFT_SCHEMA 
import pandas as pd
from pathlib import Path
import logging
from utils.config import compras_file,data_quotes,stock_file,ventas_file, list_prices_file,monetized_stock_file

# Configure logging.
logging.basicConfig(level=logging.INFO)

def load_data(file: str):

    """
    Reads the specified file (CSV or Excel format) and converts it to Parquet format, returning a DataFrame.

    Args:
        file: The name of the file to be read. Must be a CSV or XLSX file.

    Returns:
         The content of the file as a DataFrame, or None if an error occurs.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file is empty or has an unsupported format.
        RuntimeError: If an error occurs during file reading or conversion.
    """

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
            logging.info("CSV file read and converted to Parquet")
            
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path, engine='openpyxl')
            df = df.apply(lambda col: col.astype(str) if col.dtype == 'object' else col)

            # Define parquet file path
            parquet_file_path = file_path.with_suffix('.parquet')
            df.to_parquet(parquet_file_path, engine='pyarrow')
            logging.info("Excel file read and converted to Parquet")
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
    
    """
    Reads the specified Parquet file, converts it to a DataFrame, and loads it into the Redshift database.

    Args:
        file (str): The name of the Parquet file (without the extension) to load into Redshift.

    Raises:
        RuntimeError: If there is an error connecting to Redshift, if the DataFrame is empty, or if there is an error loading data into Redshift.
        KeyError: If the file name does not match any table in the redshift_tables dictionary.
    """

    # Create a dictionary with different tables, and define a table to load in Redshift.
    redshift_tables = {
        stock_file : 'stock_ferrimac',
        ventas_file : 'ventas_unidades',
        list_prices_file : 'list_prices',
        monetized_stock_file: 'stock_monetized',
        data_quotes : 'data_quotes', 
        compras_file : 'compras_stock'
    }

    if file not in redshift_tables:
        raise KeyError(f"The file '{file}' does not match any known Redshift table names.")
    
    redshift_table = redshift_tables[file]
   
    # Create URL to connect with SQLAlchemy
    connection_url = f"postgresql://{REDSHIFT_USER}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}"

    # Create connection with SQLAlchemy
    engine = create_engine(connection_url)

    # Establish connection to Redshift
    try:
        with engine.connect() as connection:
            logging.info("Connection to Redshift successful.")
            result = connection.execute("SELECT current_date;")
            for row in result:
                logging.info(f"Update from Redshift: {row[0]}")
    except Exception as e:
        raise RuntimeError(f"Error connecting to Redshift: {e}")

    # Load data from parquet file
    df = load_data(file)  
    
    # Ensure load_data has error handling
    if df is None:
        raise RuntimeError("DataFrame is empty. Check if the parquet file was loaded correctly.")

    file_stem = Path(file).stem
    file_path = Path(f"./base_datos/inventario/{file_stem}.parquet")
    
    try:
        # Load DataFrame into Redshift table
        df.to_sql(redshift_table, con=engine, schema=REDSHIFT_SCHEMA, if_exists='append', index=False)
        logging.info(f"File '{file}' successfully loaded into Redshift table '{redshift_table}'.")
    except Exception as e:
        raise RuntimeError(f"Error loading data into Redshift table '{redshift_table}': {e}")