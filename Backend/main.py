from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from procesar_datos import tendencia_personas,asistencia_eventos,extraer_db_a_dataframe
from procesar_datos import personas_por_programa
from procesar_datos import duracion_promedio_sesion,duracion_std_sesion,total_personas_sesion,minima_duracion_sesion
import json

app = FastAPI()

# Configura los encabezados CORS para permitir todas las solicitudes desde localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:1234"],
    allow_credentials=True,
    allow_methods=["*"],  # Puedes ajustar esto según tus necesidades (GET, POST, etc.)
    allow_headers=["*"],  # Puedes ajustar esto según tus necesidades
)

# Resto de tu configuración de rutas y lógica de la aplicación

days = ["1","2","3","4","5","6","7","8","9"]

# Entidad Analitica
class Analisis(BaseModel):
    total: int
    promedio: int
    std: int


@app.get("/eventos/{dia}")
async def presencia_personas_evento(dia: str):
    '''
    Proceso:
    Captura de datos para grafico de personas presentes en el evento
    a lo largo de las dos horas.
    Entradas:
    numero de evento (ej. evento 1 ... evento 10)
    Salidas:
    json de los datos
    '''
    if dia in days:
        print(f"evento_{dia}")
        data = tendencia_personas(f"evento_{dia}")
        data_to_json = data.to_json(orient='split')
        return json.loads(data_to_json)
    else:
        return {"message":f"invalid day: {dia}, review your requests"}

@app.get("/asistencia/{dia}")
async def asistencia_evento(dia: str):
    '''
    Proceso:
    Captura de datos de personas que asistieron al evento
    Entradas:
    numero de evento (ej. evento 1 ... evento 10)
    Salidas:
    json de los datos
    '''
    if dia in days:
        first_data = asistencia_eventos(f"evento_{dia}")
        data = personas_por_programa(first_data)
        data_to_json = data.to_json(orient='index')
        return json.loads(data_to_json)
    else:
        return {"message":f"invalid day: {dia}, review your requests"}

@app.get("/usuarios")
async def tomar_usuarios():
    '''
    Proceso:
    Captura de los usuarios registrados en el evento
    Entradas:
    numero de evento (ej. evento 1 ... evento 10)
    Salidas:
    json de los datos
    '''
    data = extraer_db_a_dataframe("registro_usuarios")
    data_to_json = data.to_json(orient='split')
    return json.loads(data_to_json)

@app.get("/registro_evento/{dia}")
async def registro_eventos(dia: str):
    '''
    Proceso:
    Captura de datos por evento registrado
    Entradas:
    numero de evento (ej. evento 1 ... evento 10)
    Salidas:
    json de los datos
    '''
    if dia in days:
        data = extraer_db_a_dataframe(f"evento_{dia}")
        data_to_json = data.to_json(orient='split')
        return json.loads(data_to_json)
    else:
        return {"message":f"invalid day: {dia}, review your requests"}
    
@app.get("/analisis/{dia}")
async def total_personas(dia: str):
    '''
    Proceso:
    - Conteo de cantidad de personas segun el evento establecido
    - Promedio de duración en el evento
    - Desviación estandar de la duración del evento
    Entradas:
    numero de evento (ej. evento 1 ... evento 10)
    Salidas:
    json de los datos
    '''
    if dia in days:
        cantidad_de_personas = total_personas_sesion(f"evento_{dia}")
        promedio_de_duracion = duracion_promedio_sesion(f"evento_{dia}")
        standard_deviation = duracion_std_sesion(f"evento_{dia}")
        return Analisis(total = cantidad_de_personas,
                        promedio = promedio_de_duracion,
                        std = standard_deviation)
    else:
        return {"message":f"invalid day: {dia}, review your requests"}

@app.get("/menor_tiempo/{dia}")
async def minima_duracion(dia: str):
    '''
    Proceso:
    Captura la persona con el menor tiempo durante el evento
    Entradas:
    numero de evento (ej. evento 1 ... evento 10)
    Salidas:
    json con los datos
    '''
    if dia in days:
        data = minima_duracion_sesion(f"evento_{dia}")
        data_to_json = data.to_json(orient='index')
        return json.loads(data_to_json)
    else:
        return {"message":f"invalid day: {dia}, review your requests"}
