import pandas as pd
from pathlib import Path

def update_stock(stock_file: str, compras_file: str, ventas_file: str, fecha: str):
    # Directorio donde se encuentran los archivos
    base_dir = './base_datos/inventario'
    base_path = Path(base_dir)
    
    # Cargar los archivos
    stock_path = base_path / stock_file
    compras_path = base_path / compras_file
    ventas_path = base_path / ventas_file
    
    if stock_path.exists() and compras_path.exists() and ventas_path.exists():
        # Leer archivos de stock, compras y ventas
        df_stock = pd.read_excel(stock_path, engine='openpyxl')
        df_compras = pd.read_excel(compras_path, engine='openpyxl')
        df_ventas = pd.read_excel(ventas_path, engine='openpyxl')

        # Convertir columnas de fechas a formato datetime, para luego igualar los formatos
        df_stock.columns = pd.to_datetime(df_stock.columns, errors='ignore', dayfirst=True)
        df_compras.columns = pd.to_datetime(df_compras.columns, errors='ignore', dayfirst=True)
        df_ventas.columns = pd.to_datetime(df_ventas.columns, errors='ignore', dayfirst=True)
        
        # Convertir la fecha dada a formato datetime
        fecha = pd.to_datetime(fecha, format='%Y-%m-%d')

        
        # Verificar si la fecha está en los datos
        if fecha not in df_stock.columns or fecha not in df_compras.columns or fecha not in df_ventas.columns:
            print(f"La fecha {fecha} no está presente en los archivos.{df_stock.columns}")
            return
        
        # Obtener la columna del día anterior al último
        #fecha_anterior = df_stock.columns[-1]
        
        # Actualizar stock: stock día anterior + compras - ventas
        df_stock[fecha] = df_stock[fecha] + df_compras[fecha] - df_ventas[fecha]
        
        # Guardar el archivo de stock actualizado
        df_stock.to_excel(stock_path, index=False)
        
        print(f"El archivo de stock ha sido actualizado para la fecha {fecha}. and ")
    else:
        print("Uno o más archivos no existen. Verifica los nombres y las rutas.")
