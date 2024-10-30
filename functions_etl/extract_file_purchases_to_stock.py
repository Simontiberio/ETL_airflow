import os
import shutil
from datetime import datetime
from pathlib import Path
from utils.config import compras_file
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_file_purchases_to_stock( file_compras : str ):


    """
    Extracts and moves the specified purchases file to the inventory directory.
    
    Args:
        file_compras (str): Name of the purchases file to move.
        
    Logs:
        - Errors if the source or destination directories do not exist.
        - Information confirming the successful move of the file.
        - Warnings if the specified file does not exist in the source directory.
    """



    # Define directory path.
    base_dir = './base_datos/'
    base_path = Path(base_dir)

    # Define origin and destination paths.
    origin_path = base_path.joinpath('compras')
    destination_path = base_path.joinpath('inventario')

    # Verified if exist origin and destination paths.
    if not origin_path.exists():
        logging.error(f"Directory {origin_path} not found.")
        return
        
    if not destination_path.exists():
        logging.error(f"Destination directory {destination_path} not found.")
        return
        
    # Origin path define complete.
    archivo_origen = origin_path.joinpath(file_compras)
    
    # Check if the file exists in the defined path.
    if archivo_origen.exists():
        archivo_destino = destination_path.joinpath(file_compras)

        # Copy origin file to destination.
        
        shutil.copy(str(archivo_origen), str(archivo_destino))
        logging.info(f"File '{file_compras}' moved to stock folder successfully.")
        
    else:
        logging.warning(f"The file '{file_compras}' was not found in the purchases directory.")
        

