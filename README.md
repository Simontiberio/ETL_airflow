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

El pipeline se estructura en 3 etapas o fases:

Extraccion de datos

En esta etapa, se realiza la extracción y recoleccion de los datos. Esta compuesto por 3 tareas, las cuales se ejecutan en paralelo.

 :one:```def append_to_data_price: ``` Se obtiene diariamente, mediante el uso de una API la cotizacion del dolar oficial. Una vez obtenido el precio de la fecha, actualiza el dataframe que almacena la historia de la divisa.

 :two:```def extract_file_sells_to_stock:```Recupera en forma diaria, del subdominio de ventas, las unidades vendidas del ultimo dia habil. Se obtiene la informacion al cierre del dia, incluyendo el movimiento de la jornada.

 :three:```def extract_file_purchases_to_stock:```Recupera en forma diaria, del subdominio de compras, las compras de mercaderia/productos realizadas a distintos proveedores. Actualiza aquellas compras que han sido conformadas y recepcionadas en inventario.Se obtiene la informacion al cierre de la jornada, incluyendo el movimiento del dia.

 Transformacion 

 En este paso, el pipeline realizara tareas de transformacion y calculo de los datos recolectados en la etapa anterior.

 :one:```def update_stock: ```A fin de poder valuar el stock de productos, tomamos como input el stock actual, unidades vendidas, las compras realizadas. La funcion update_stock, actualizara las unidades de stock, contemplando el movimiento del dia, es decir las unidades que se vendieron y los productos recibidos por las compras realizadas.





