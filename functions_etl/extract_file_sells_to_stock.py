import os
import shutil
from datetime import datetime
from pathlib import Path
from utils.config import ventas_file

def extract_file_sells_to_stock(file_ventas: str ):
    # Define directory path.
    
    base_dir = './base_datos/'
    base_path = Path(base_dir)

    # Define origin and destination paths.

    origin_path = base_path.joinpath('ventas')
    destination_path = base_path.joinpath('inventario')

    # Verified if exist origin and destination paths.
    if not origin_path.exists():
        print(f"Directory {origin_path} not exist.")
        return
    if not destination_path.exists():
        print(f" Directory {destination_path} not exist.")
        return

   # Origin path define complete.

    archivo_origen = origin_path.joinpath(file_ventas)
    
     # Check if the file exists in the defined path.
    if archivo_origen.exists():
        archivo_destino = destination_path.joinpath(file_ventas)

        # Copy origin file to destination.
        shutil.copy(str(archivo_origen), str(archivo_destino))
        print(f"File '{file_ventas}' moved to stock folder correctly.")
    else:
        print(f"The file '{file_ventas}' was not found in the sells directory.")