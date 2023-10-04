# PASOS PARA CREAR LA BASE DE DATOS

1. Ejecutar en la ruta "ETL/src/limpieza.ipynb"
2. Ejecutar en la ruta "ETL/src/" create_db.py
3. Ejecutar en la ruta "ETL/src" config_db.py

## Archivo database.sql

En la ruta "ETL/src/" se encuentra database.sql que contiene querys que nos sirven para
la creación de la base de datos y sus tablas en PostgreSQL como alternativa a los pasos 2 y 3 anteriores.
Ademas de al momento de cargar la data se encuentra en la ruta "ETL/clean_data" y son los siguientes archivos:

- En la tabla registro_usuarios: se carga registro_usuarios.csv
- En la tabla evento_dia_06: se carga evento_dia_06.csv
- En la tabla evento_dia_08: se carga evento_dia_08.csv
- En la tabla evento_dia_13: se carga evento_dia_13.csv
- En la tabla evento_dia_15: se carga evento_dia_15.csv

_Nota: tener presente las llaves foranes y primarias ya que alguna data no se encuentra en la principal registro usuarios, por ende se perdera esa data_
