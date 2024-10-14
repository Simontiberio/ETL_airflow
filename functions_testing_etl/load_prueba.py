from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from utils.config import REDSHIFT_HOST,REDSHIFT_DB,REDSHIFT_PORT,REDSHIFT_USER,REDSHIFT_PASSWORD, REDSHIFT_SCHEMA
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from pathlib import Path





def load_prueba(file: str):

    '''It is a function that reads the file depending on its format, and stores it in a df. 
    It is a function that is used in the load_data_to_redshift function to load said df as a table in the DB.'''


    # Get extesion file.

    file_extension = Path(file).suffix.lower()
    
    # Define the path of file.
    file_path = Path(f"./base_datos/inventario/{file}")

    # Check if the file exist.
    if not file_path.exists():
        print(f"Error: File'{file_path}' not found.")
        return None

    # initialized dataframe.
    df = None

    # Read files depending on the formats.
    try:
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
            df = df.apply(lambda col: col.astype(str) if col.dtype == 'object' else col)
            file = Path(file).stem
            file_path = Path(f"./base_datos/inventario/{file}")
            df = df.to_parquet(f"{file_path}.parquet", engine='pyarrow')
            print("File read as parquet")
            
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path, engine='openpyxl')
            df = df.apply(lambda col: col.astype(str) if col.dtype == 'object' else col)
            file = Path(file).stem
            file_path = Path(f"./base_datos/inventario/{file}")
            df = df.to_parquet(f"{file_path}.parquet", engine='pyarrow')
            print("File read as parquet")
        else:
            print("File format not supported. Check if use as CSV or XLSX file.")
            return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    # Check if the dataframe was loaded correctly.
    if df is not None:
        return df
    else:
        print("Failed to load file.")
        return None
    
    




def load_data_to_Redshift_prueba (file : str, redshift_table : str ) :

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

    df = load_prueba(file)
    file = Path(file).stem
    file_path = Path(f"./base_datos/inventario/{file}")
    df = pd.read_parquet(f"{file_path}.parquet")
   
    df.to_sql(redshift_table, con=engine, schema= REDSHIFT_SCHEMA, if_exists='append', index=False)

    print(f"File loaded into Redshift table {redshift_table}")