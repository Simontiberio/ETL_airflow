import os
from pathlib import Path
import pandas as pd

def transform_data (file1: str, file2: str): 
 
    base_dir = './base_datos/'
    base_path = Path(base_dir)
    file1_path = base_path / file1
    file2_path = base_path / file2
    
     
    if file1_path.exists() and file2_path.exists():
        # Read files.
        df1 = pd.read_excel(file1_path,engine='openpyxl')
        df2 = pd.read_csv(file2_path)


        # Get lasted record of prices dataset.
        df2['date'] = pd.to_datetime(df2['date'])
        latest_record = df2.sort_values(by='date').iloc[-1]

        # Transform last record to df.
        latest_record_df = pd.DataFrame([latest_record])  #
        
        # Concancate both df and calculate total amount in pesos.
        df_transform = pd.concat([df1, latest_record_df], ignore_index=True)
        df_transform['date'] = latest_record_df['date'].iloc[0]
        df_transform['price'] = round(df2['price'].iloc[0],2)
        df_transform['total_amount'] = df_transform['price'] * df_transform['Quantity']
                          
        # Save the changes in 'File 1'
        df_transform.to_excel(file1_path, index=False)
        
        print(f"The files have been successfully concatenated and saved to {file1_path}")
    else:
        print("One or both files do not exist. Check names and paths.")