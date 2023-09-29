import psycopg2
from decouple import config
import csv

conn = psycopg2.connect(host="localhost", password=config(
    'PASSWORD'), user="postgres", port=5432)
cursor = conn.cursor()


def create_database(db_name):
    try:
        conn.autocommit = True
        cursor.execute(f"CREATE DATABASE {db_name}")
        conn.autocommit = False
        print(f"La base de datos {db_name} ha sido creada exitosamente!")
    except psycopg2.DatabaseError as e:
        print(f"Error al crear la base de datos: {e}")


# create_database("eventos")
conn.close()

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

eventos = ["evento_dia_06", "evento_dia_08", "evento_dia_13", "evento_dia_15"]

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

archivos = ["evento_dia_06.csv", "evento_dia_08.csv",
            "evento_dia_13.csv", "evento_dia_15.csv"]

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
