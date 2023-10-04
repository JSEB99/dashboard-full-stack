-- Crear Base de datos
CREATE DATABASE eventos
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Colombia.1252'
    LC_CTYPE = 'Spanish_Colombia.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Crear tabla de registros
CREATE TABLE IF NOT EXISTS registro_usuarios (
                nombre VARCHAR(50),
                correo VARCHAR(50) PRIMARY KEY,
                programa_academico VARCHAR(50),
                asignatura VARCHAR(50),
                estado VARCHAR(20),
                primer_nombre VARCHAR(15),
                primer_apellido VARCHAR(15));

-- Crear tablas de eventos
-- Cambiar el nombre por el día del evento
-- EVENTOS: 
-- evento_dia_06,evento_dia_08,evento_dia_13,evento_dia_15
CREATE TABLE IF NOT EXISTS evento_dia_06 (
                ID_evento serial PRIMARY KEY,
                Nombre VARCHAR(50),
                Apellido VARCHAR(50),
                "Correo electrónico" VARCHAR(50),
                "Hora a la que se unió" TIMESTAMP,
                "Hora a la que salió" TIMESTAMP,
                NombreCompleto VARCHAR(50),
                duración SMALLINT,
                FOREIGN KEY ("Correo electrónico") REFERENCES registro_usuarios(correo));

-- Cargue de los datos de registro_usuarios en PostgreSQL
\COPY registro_usuarios(nombre, correo, programa_academico, asignatura, estado, primer_nombre, primer_apellido)
FROM 'C:/ruta/al/archivo.csv' WITH CSV HEADER DELIMITER ',';

-- Utiliza una transacción para realizar la carga
BEGIN;

-- Carga los datos desde el archivo CSV en la tabla evento_dia_06
\COPY evento_dia_06 (
    Nombre, Apellido, "Correo electrónico", "Hora a la que se unió", "Hora a la que salió", NombreCompleto, duración
) FROM 'C:/ruta/al/archivo.csv' WITH CSV HEADER DELIMITER ',';

-- Termina la transacción
COMMIT;



