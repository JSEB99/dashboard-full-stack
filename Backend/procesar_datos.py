import pandas as pd 
from sqlalchemy import create_engine
from decouple import Config,RepositoryEnv
import json
import datetime

config = Config(RepositoryEnv(r"C:\Users\Usuario\Desktop\DB - UPTC\Proyecto_ETL_Dashboard\Backend\.env"))

def extraer_db_a_dataframe(tabla):
    host = "localhost"
    password = config("PASSWORD")
    user = "postgres"
    dbname = "eventos"
    port = 5432

    db_uri = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

    engine = create_engine(db_uri)
    
    sql_query = f"SELECT * FROM {tabla}"

    df = pd.read_sql_query(sql_query, engine)

    # Cerrar conexión
    engine.dispose()

    return df

def asistencia_eventos(dataframe_db):
    registro_usuarios = extraer_db_a_dataframe("registro_usuarios")
    dataframe_input = extraer_db_a_dataframe(dataframe_db)
    dataframe_output = pd.merge(registro_usuarios,dataframe_input,how='left',left_on='correo',right_on='Correo electrónico')
    dataframe_output = dataframe_output.dropna(subset=["Correo electrónico"])[["nombre_x","correo","programa_academico","asignatura","estado","Hora a la que se unió","Hora a la que salió","duración"]]
    dataframe_output = dataframe_output[dataframe_output["estado"] != "Falta información"]
    dataframe_output.rename(columns={'nombre_x':'nombre_completo',
                                     'Hora a la que se unió':"hora_entrada",
                                     'Hora a la que salió':"hora_salida"
                                     },inplace=True)
    return dataframe_output[["nombre_completo","correo","programa_academico","asignatura","estado","hora_entrada","hora_salida","duración"]]

# Convierte las columnas "hora_entrada" y "hora_salida" en objetos datetime
def tendencia_personas(df_db):
    dataframe_out = asistencia_eventos(df_db)
    dataframe_out['hora_entrada'] = pd.to_datetime(dataframe_out['hora_entrada'])
    dataframe_out['hora_salida'] = pd.to_datetime(dataframe_out['hora_salida'])

    # Crea una lista de eventos que registra la entrada de una persona como +1 y la salida como -1
    eventos = [(hora, programa, 1) for hora, programa in zip(dataframe_out['hora_entrada'], dataframe_out['programa_academico'])] + \
            [(hora, programa, -1) for hora, programa in zip(dataframe_out['hora_salida'], dataframe_out['programa_academico'])]

    # Crea un DataFrame_out a partir de la lista de eventos
    df_eventos = pd.DataFrame(eventos, columns=['hora', 'programa_academico', 'evento'])

    # Ordena los eventos por hora
    df_eventos = df_eventos.sort_values(by='hora')

    # Calcula la cantidad acumulada de personas presentes en cada minuto
    df_eventos['personas_presentes'] = df_eventos.groupby('programa_academico')['evento'].cumsum()
    
    # Hora lo convierto en string
    df_eventos["hora"] = df_eventos["hora"].astype(str)

    # Ajusto columnas de salida
    df_eventos = df_eventos.pivot_table(index='hora',columns='programa_academico',values='personas_presentes').interpolate(method='linear').fillna(0) 
    # # Hora se vuelve columna
    # df_eventos.reset_index(inplace=True)
    return df_eventos

def personas_por_programa(dataframe):
    dataframe_out = dataframe.groupby("programa_academico").count()
    dataframe_out.reset_index(inplace=True)
    dataframe_out.rename(columns={'nombre_completo':'cantidad_personas'},inplace=True)
    return dataframe_out[["programa_academico","cantidad_personas"]]

def duracion_promedio_sesion(dataframe):
    dataframe_out = asistencia_eventos(dataframe)
    return int(round(dataframe_out["duración"].mean()))

def duracion_std_sesion(dataframe):
    dataframe_out = asistencia_eventos(dataframe)
    return int(round(dataframe_out["duración"].std()))

def total_personas_sesion(dataframe):
    preprocess = asistencia_eventos(dataframe)
    dataframe_out = personas_por_programa(preprocess)
    return dataframe_out["cantidad_personas"].sum()

def minima_duracion_sesion(dataframe):
    dataframe_out = asistencia_eventos(dataframe)
    min_duration = dataframe_out["duración"].min()
    return dataframe_out[["nombre_completo","duración","correo"]].loc[dataframe_out["duración"]==min_duration]

if __name__=="__main__":
    # registro_usuarios = extraer_db_a_dataframe_out("registro_usuarios")
    # print(registro_usuarios)


    evento_dia_06 = extraer_db_a_dataframe("evento_dia_06")
    asistencia_dia_06 = asistencia_eventos("evento_dia_06")
    # print(asistencia_dia_06)
    evento_06 = tendencia_personas("evento_dia_06")
    jsonsito = evento_06.to_json(orient='split')
    datason = json.loads(jsonsito)
    #print(personas_por_programa(asistencia_dia_06))
    print(duracion_promedio_sesion("evento_dia_06"))
    print(duracion_std_sesion("evento_dia_06"))
    print(total_personas_sesion("evento_dia_06"))
    print(minima_duracion_sesion("evento_dia_06"))
