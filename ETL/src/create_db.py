import psycopg2
from decouple import config

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


create_database("eventos")
conn.close()