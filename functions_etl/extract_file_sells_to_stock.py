import os
import shutil
from datetime import datetime
from pathlib import Path
from utils.config import ventas_file
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_file_sells_to_stock(file_ventas: str ):

    """
    Extracts and moves the specified sales file to the inventory directory.
    
    Args:
        file_ventas: Name of the sales file to move.
        
    Logs:
        - Errors if the source or destination directories do not exist.
        - Information confirming the successful move of the file.
        - Warnings if the specified file does not exist in the source directory.
    """


    # Define directory path.
    base_dir = './base_datos/'
    base_path = Path(base_dir)
    
    # Define origin and destination paths.

    origin_path = base_path.joinpath('ventas')
    destination_path = base_path.joinpath('inventario')
    logging.info(f"Origin directory: {origin_path}")
    logging.info(f"Destination directory: {destination_path}")


    # Verified if exist origin and destination paths.
    if not origin_path.exists():
        logging.error(f"Directory {origin_path} does not exist.")
        return

    if not destination_path.exists():
        logging.error(f"Directory {destination_path} does not exist.")
        return
       
   # Origin path define complete.

    archivo_origen = origin_path.joinpath(file_ventas)
    logging.info(f"Origin file path set to '{archivo_origen}'")

     # Check if the file exists in the defined path.
    if archivo_origen.exists():
        archivo_destino = destination_path.joinpath(file_ventas)
        logging.info(f"Destination file path set to '{archivo_destino}'")
        try:
            # Copy origin file to destination.
            shutil.copy(str(archivo_origen), str(archivo_destino))
            logging.info(f"File '{file_ventas}' moved to stock folder successfully.")
        except PermissionError as e:
            logging.error(f"PermissionError while copying file: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
    else:
        logging.warning(f"The file '{file_ventas}' was not found in the sales directory.")
        