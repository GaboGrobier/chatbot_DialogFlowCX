from fastapi import FastAPI , Request,HTTPException
import jwt
from decouple import  config
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from rutas.formateo import formateo_respuesta
from rutas.manejador_acciones import intencion_bienvenida, intencion_postulante


app = FastAPI()

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"


class Token(BaseModel):
    access_token: str


#verificar Token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None


@app.post("/webhook", response_model=dict)
async def enviarmensaje(request: Request):
    token = request.headers.get('Authorization')
    if token is None:
        error = formateo_respuesta(['Sin autorización, contacta un Administrador '])
        return jsonable_encoder(error)
    payload = verify_token(token)
    if payload is None:
        error = formateo_respuesta(['Sin autorización '])
        return jsonable_encoder(error)

    body = await request.json()
    action = body['queryResult']['action']
# Obtener los parámetros de outputContexts
    output_contexts = body.get("queryResult", {}).get("outputContexts", [])

    #Inicializar las variables
    ubicacion = None
    estado = None
    carrera = None

    # Iterar sobre los contextos y obtener los parámetros
    for context in output_contexts:
        parametros = context.get("parameters", {})
        ubicacion = parametros.get("Ubicacion") or ubicacion
        estado = parametros.get("Estado") or estado
        carrera = parametros.get("Carrera") or carrera


    if action == 'Bienvenida':
        print('esto en ', action)
        response = intencion_bienvenida(body)
        return jsonable_encoder(response)

    if action == 'postulante':
        response = intencion_postulante(body)
        return jsonable_encoder(response)

    else:
        return jsonable_encoder(
            formateo_respuesta(
                ['No he podido entender tu pregunta por favor realizala de nuevo ']
            )
        )
