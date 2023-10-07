import psycopg2
import pandas as pd
from decouple import config
import csv

conn2 = psycopg2.connect(host="localhost", dbname="eventos", password=config(
    'PASSWORD'), user="postgres", port=5432)
cursor = conn2.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS registro_usuarios (
                nombre VARCHAR(50),
                correo VARCHAR(50) PRIMARY KEY,
                programa_academico VARCHAR(50),
                asignatura VARCHAR(50),
                estado VARCHAR(20),
                primer_nombre VARCHAR(15),
                primer_apellido VARCHAR(15)
)""")
conn2.commit()

eventos = ["evento_1", "evento_2", "evento_3", "evento_4",
           "evento_5", "evento_6", "evento_7", "evento_8", "evento_9"]

for evento in eventos:
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {evento} (
                ID_evento serial PRIMARY KEY,
                Nombre VARCHAR(50),
                Apellido VARCHAR(50),
                "Correo electrónico" VARCHAR(50),
                "Hora a la que se unió" TIMESTAMP,
                "Hora a la que salió" TIMESTAMP,
                NombreCompleto VARCHAR(50),
                duración SMALLINT,
                FOREIGN KEY ("Correo electrónico") REFERENCES registro_usuarios(correo)
    )""")
    conn2.commit()


with open("../clean_data/registro_usuarios.csv", "r", encoding="UTF-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Inserta cada fila en la tabla registro_usuarios
        cursor.execute(
            """INSERT INTO registro_usuarios
            (nombre, correo, programa_academico, asignatura, estado, primer_nombre, primer_apellido)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                row['Nombre'],
                row['Correo institucional (@uptc.edu.co)'],
                row['Programa Académico'],
                row['Asignatura'],
                row['estado'],
                row['Primer Nombre'],
                row['Primer Apellido']
            )
        )
conn2.commit()

archivos = [
    "evento_1.csv",
    "evento_2.csv",
    "evento_3.csv",
    "evento_4.csv",
    "evento_5.csv",
    "evento_6.csv",
    "evento_7.csv",
    "evento_8.csv",
    "evento_9.csv",
]

# Crear un DataFrame vacío para almacenar las filas no insertadas
filas_no_insertadas = pd.DataFrame(columns=["Nombre", "Apellido", "Correo electrónico",
                                   "Hora a la que se unió", "Hora a la que salió", "NombreCompleto", "duración"])

for archivo in archivos:
    with open(f"../clean_data/{archivo}", "r", encoding="UTF-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            correo = row["Correo electrónico"]

            # Verifica si el correo existe en la tabla registro_usuarios
            cursor.execute(
                "SELECT 1 FROM registro_usuarios WHERE correo = %s", (correo,))
            exists = cursor.fetchone()

            if exists:
                # Inserta la fila en la tabla evento_dia_06
                sql_query = f"""INSERT INTO {archivo[:-4]}
                    ("nombre", "apellido", "Correo electrónico", "Hora a la que se unió", "Hora a la que salió", "nombrecompleto", "duración")
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                cursor.execute(sql_query, (
                    row['Nombre'],
                    row['Apellido'],
                    correo,
                    row['Hora a la que se unió'],
                    row['Hora a la que salió'],
                    row['NombreCompleto'],
                    row['duración']
                ))

                conn2.commit()
            else:
                print(
                    f"El correo {correo} no existe en la tabla registro_usuarios. La fila no se insertará.")
                # Agregar la fila al DataFrame de filas no insertadas
                filas_no_insertadas = pd.concat(
                    [filas_no_insertadas, pd.DataFrame([row])], ignore_index=True)


# O guardar el DataFrame de filas no insertadas como Excel
filas_no_insertadas.to_excel(
    "../clean_data/filas_no_insertadas.xlsx", index=False)
