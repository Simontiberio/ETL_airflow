# :rocket: Proyecto ETL - Ferrimac :hammer: :wrench:

## :memo: Descripción del Proyecto

Este proyecto de ETL (Extract, Transform, Load) está diseñado para un caso de negocio,Ferretería **Ferrimac**. Utiliza Apache Airflow para automatizar y orquestar tareas de extracción, transformación y carga de datos provenientes de una API y de archivos locales. El objetivo es generar informacion de valor para su dueño, que del total de informacion de sistema, poder armar una vista del stock valorizado en pesos, calculando el valor de los productos en inventario según su precio en dólares y la cotización diaria del dólar.

El pipeline incluye múltiples tareas (tasks) en Airflow, encargadas de extraer la información de ventas y compras, actualizar el stock, valorizarlo, y cargar los datos en una base de datos Redshift.


## Estructura del Proyecto 




## :desktop_computer: :gear: Pasos de Configuración 

1- Clonar el repositorio.

```bash
# Comando para clonar el repositorio
git clone git@github.com:Simontiberio/ETL_airflow.git

```

2- Crear un archivo .env con las configuraciones necesarias, incluyendo las credenciales de la API y las rutas de los archivos de ventas y compras.


```bash
# UID AIRFLOW.

AIRFLOW_UID=1000

# Credenciales Redshift.

REDSHIFT_USER= '2024_nombre_apellido'
REDSHIFT_PASSWORD='PASSWORD'
REDSHIFT_DB= 'NOMBRE_DB'
REDSHIFT_HOST='REDSHIFT_HOST'
REDSHIFT_PORT= PORT

# Variables de entorno.

REDSHIFT_SCHEMA = 'REDSHIFT_SCHEMA'

api_key = 'your_api_key'

compras_file = 'nombre_archivo.xlsx'
stock_file = 'nombre_archivo.xlsx'
ventas_file = 'nombre_archivo.xlsx'
monetized_stock_file = 'nombre_archivo.xlsx'
data_quotes = 'nombre_archivo.csv'
list_prices_file = 'nombre_archivo.xlsx'

```
3- Iniciar los servicios de Airflow utilizando Docker Compose:

```
docker-compose up -d
```

4- Acceder a la interfaz de Airflow en http://localhost:8080 y activar el DAG llamado etl_update_stock_ferrimac.


### Estructura del Pipeline 

El pipeline de Airflow se compone de tres fases principales:

1. Extracción de Datos

En esta etapa, se recolectan los datos mediante tres tareas ejecutadas en paralelo:

``` def append_to_data_price():```: Obtiene diariamente la cotización del dólar desde una API, actualizando un archivo histórico de cotizaciones.

``` def extract_file_sells_to_stock (): ``` Extrae las ventas diarias del sistema de ventas al cierre de cada jornada.

``` def extract_file_purchases_to_stock ():``` Recupera las compras de productos a distintos proveedores, actualizando el inventario con las compras recepcionadas.

2. Transformación de Datos

Aquí se transforman los datos para calcular el valor del stock.

``` def update_stock (): ```: Actualiza el stock diario considerando las ventas y compras registradas.

``` def monetize_stock ():``` Valoriza el stock actualizado utilizando la última lista de precios en dólares y la cotización del día.

3. Carga de Datos

En esta última etapa, los datos son almacenados y cargados en Redshift.

``` def load_data ():``` Convierte el stock valorizado a formato Parquet para un almacenamiento más eficiente.

``` def load_data_to_Redshift ():``` Carga el archivo Parquet a la base de datos Redshift, ubicada en un cluster de AWS.



![Arquitectura y dependencias del Pipeline](images/arquitectura_pipeline.png)





