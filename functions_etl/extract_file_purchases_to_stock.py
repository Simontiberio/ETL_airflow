import os
import shutil
from datetime import datetime
from pathlib import Path

def extract_file_purchases_to_stock(archivo : str ):
    # Define directory path.
    base_dir = './base_datos/'
    base_path = Path(base_dir)

    # Define origin and destination paths.
    origin_path = base_path.joinpath('compras')
    destination_path = base_path.joinpath('inventario')

    # Verified if exist origin and destination paths.
    if not origin_path.exists():
        return print(f"El directorio {origin_path} no existe.")
    if not destination_path.exists():
        
        return print(f"El directorio {destination_path} no existe.")

    # Origin path define complete.
    archivo_origen = origin_path.joinpath(archivo)
    
    # Check if the file exists in the defined path.
    if archivo_origen.exists():
        archivo_destino = destination_path.joinpath(archivo)

        # Copy origin file to destination.
        
        shutil.copy(str(archivo_origen), str(archivo_destino))
        print(f"File '{archivo}' moved to stock folder correctly.")
    else:
        print(f"The file '{archivo}' was not found in the purchases directory.")

