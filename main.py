from fastapi import FastAPI , Request
import jwt
from decouple import  config
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from rutas.formateo import formateo_respuesta
from rutas.manejador_acciones import intencion_bienvenida, intencion_postulante
from rutas.manejador_acciones import interactuar_con_hugchat
from fastapi.responses import JSONResponse



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
#

@app.post("/webhook", response_model=dict)
async def enviarmensaje(request: Request):
    #obtencion de token enviado de plataforma
    token = request.headers.get('Authorization')
    #Validacion token vacio
    if token is None:
        error = formateo_respuesta(['Sin autorización, contacta un Administrador '])
        return jsonable_encoder(error)

    #validacion token sin permiso
    payload = verify_token(token)
    if payload is None:
        error = formateo_respuesta(['Sin autorización '])
        return jsonable_encoder(error)

#obtener valores principales de trabajo
    body = await request.json()
    print(body)
    # Obtener la información del intento
    intent_info = body.get('intentInfo', {})
    display_name = intent_info.get('displayName', '')
    tag = body.get('fulfillmentInfo',{}).get('tag','')
    print('este es el tag---->',tag)

    # Imprimir el nombre del intento
    print('Display Name:', display_name)



#intencion de bienvenida - primer ingreso
    if display_name == 'Bienvenida':
        response = intencion_bienvenida(body)
        return jsonable_encoder(response)

#Solicitud de postulantes
    if display_name == 'Solicitud_postulante':
        parameters = intent_info.get('parameters', {})
        region = parameters.get('region', {}).get('resolvedValue', '')
        carrera = parameters.get('carrera', {}).get('resolvedValue', '')

        # Imprimir los valores obtenidos
        print('Region:', region)
        print('Carrera:', carrera)
        response = intencion_postulante(carrera, region)
        print(response)
        return response




#intencion de backup - modo prueba
    if tag == 'Respuesta_hugchat':
        mensaje = body.get("text", {})
        print(mensaje)

        # Llama a HugChat de manera asincrónica
        response_hugchat =  str(interactuar_con_hugchat(mensaje))
        print(response_hugchat)
        respuesta = formateo_respuesta([response_hugchat])
        print(respuesta)


        return respuesta

