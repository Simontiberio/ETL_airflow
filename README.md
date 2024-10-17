# :rocket: Proyecto ETL - Ferrimac :hammer: :wrench:

## :memo: Descripción del Proyecto

Este proyecto de ETL (Extract, Transform, Load) está diseñado para un caso de negocio,Ferretería **Ferrimac**. Utiliza Apache Airflow para automatizar y orquestar tareas de extracción, transformación y carga de datos provenientes de una API y de archivos locales. El objetivo es generar informacion de valor para su dueño, que del total de informacion de sistema, poder armar una vista del stock valorizado en pesos, calculando el valor de los productos en inventario según su precio en dólares y la cotización diaria del dólar.

El pipeline incluye múltiples tareas (tasks) en Airflow, encargadas de extraer la información de ventas y compras, actualizar el stock, valorizarlo, y cargar los datos en una base de datos Redshift.


## Estructura del Proyecto 


## Arquitectura del Pipeline ETL en Airflow




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


## Estructura del Pipeline 

![Diagrama del pipeline ETL](./utils/images/pipeline-image.png)

