import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from utils.config import api_key, compras_stock,data_quotes,stock_ferrimac,ventas_unidades, monetized_stock, REDSHIFT_SCHEMA
from functions_etl.obtain_currency import append_to_data_price
from functions_etl.extract_file_purchases_to_stock import extract_file_purchases_to_stock
from functions_etl.extract_file_sells_to_stock import extract_file_sells_to_stock
from functions_etl.update_stock import update_stock
from functions_etl.data_transform import monetize_stock
from functions_etl.load_data import load_data_to_Redshift

# Define DAG.

with DAG (
    'etl_update_stock_ferrimac',
    default_args= {
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
    },
    description='ETL pipeline to extract,transform and load data into redshift',
    schedule_interval= '@daily',
    start_date= datetime(2024,1,1),
    catchup= False,
) as dag: 
    pass 


    # Task 1 : Extract data from API.

    extract_task_API = PythonOperator( 
        task_id = 'extract_task_api',
        python_callable = append_to_data_price,
        op_kwargs= {'api_key': api_key , 'file' : data_quotes }
    )

    # Task 2 : Extract data from sells directory.

    extract_data_sells_directory = PythonOperator( 
        task_id = 'extract_data_sells_directory',
        python_callable = extract_file_sells_to_stock,
        op_kwargs= {'file' : ventas_unidades }
    )

    # Task 3 : Extract data from purchases directory.

    extract_data_purchases_directory = PythonOperator( 
        task_id = 'extract_data_purchases_directory',
        python_callable = extract_file_purchases_to_stock,
        op_kwargs= {'file' : compras_stock}
    )

    # Task 4 : Transform data, stock update from purchases and units sold.

    transform_data_update_stock = PythonOperator( 
        task_id = 'stock_update',
        python_callable = update_stock,
        op_kwargs= {'file' : stock_ferrimac,
                    'file' : compras_stock,
                    'file' : ventas_unidades,
                    'date' : '{{ ds }}' }
    )

    # Task 5 : Transform data, monetize stock using list of prices and data quotes.

    transform_data_monetize_stock = PythonOperator( 
        task_id = 'monetized_stock',
        python_callable = monetize_stock,
        op_kwargs= {'file' : stock_ferrimac,
                    'file' : data_quotes,
                    'date' : '{{ ds }}' }
    )


    # Task 6 : Load data into Redshift.

    load_data_monetize_stock = PythonOperator( 
        task_id = 'load_data_into_Redshif',
        python_callable = load_data_to_Redshift,
        op_kwargs= {'file' : monetized_stock,
                    'redshift_table' : 'monetized_stock'
                 }
    )

    # Set task dependencies.

    [extract_task_API,extract_data_sells_directory,extract_data_purchases_directory] >> transform_data_update_stock >> transform_data_monetize_stock >> load_data_monetize_stock