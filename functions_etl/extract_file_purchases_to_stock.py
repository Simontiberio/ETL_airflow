import os
import shutil
from datetime import datetime
from pathlib import Path

def extract_file_purchases_to_stock(file : str ):
    # Define directory path.
    base_dir = './base_datos/'
    base_path = Path(base_dir)

    # Define origin and destination paths.
    origin_path = base_path.joinpath('compras')
    destination_path = base_path.joinpath('inventario')

    # Verified if exist origin and destination paths.
    if not origin_path.exists():
        return print(f"Directory  {origin_path} not found.")
    if not destination_path.exists():
        
        return print(f"Directory  {destination_path} not found.")

    # Origin path define complete.
    archivo_origen = origin_path.joinpath(file)
    
    # Check if the file exists in the defined path.
    if archivo_origen.exists():
        archivo_destino = destination_path.joinpath(file)

        # Copy origin file to destination.
        
        shutil.copy(str(archivo_origen), str(archivo_destino))
        print(f"File '{file}' moved to stock folder correctly.")
    else:
        print(f"The file '{file}' was not found in the purchases directory.")

