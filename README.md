# :rocket: Proyecto ETL - Ferrimac :rocket:

## Descripción del Proyecto

Este proyecto de ETL (Extract, Transform, Load) está diseñado para un caso de negocio,Ferretería **Ferrimac**. Utiliza Apache Airflow para automatizar y orquestar tareas de extracción, transformación y carga de datos provenientes de una API y de archivos locales. El objetivo es generar informacion de valor para su dueño, que del total de informacion de sistema, poder armar una vista del stock valorizado en pesos, calculando el valor de los productos en inventario según su precio en dólares y la cotización diaria del dólar.

El pipeline incluye múltiples tareas (tasks) en Airflow, encargadas de extraer la información de ventas y compras, actualizar el stock, valorizarlo, y cargar los datos en una base de datos Redshift.




## Requisitos


