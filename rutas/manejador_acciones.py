from rutas.formateo import formateo_respuesta
import os
from decouple import config
import asyncio
from sydney import SydneyClient
os.environ["BING_U_COOKIE"]=config('bing_chat_key')
import requests
import json



#configuracion intencion de bienvenida
def intencion_bienvenida(body : dict)->dict :
#    session = body['session']
#    print('esta es la session',session)


    respuesta = formateo_respuesta(
        [
            'Hola seré tu asistente de TalentQuest ',
            'Necesito que me indiques minimo 1 carrera y region de donde buscas tus candidatos ',

        ]
    )
    return respuesta

#configuracion accion para intencion de solicitud de postulante
def intencion_postulante(body: dict)->dict:
    # Obtener los parámetros de outputContexts
    output_contexts = body.get("queryResult", {}).get("outputContexts", [])

    #Inicializar las variables
    ubicacion = None
    estado = None
    carrera = None
    cantidad = None

    # Iterar sobre los contextos y obtener los parámetros
    for context in output_contexts:
        parametros = context.get("parameters", {})
        ubicacion = ', '.join(parametros.get("Ubicacion", []))  # Convertir la lista en una cadena limpia
        carrera = ', '.join(parametros.get("Carrera", []))  # Convertir la lista en una cadena limpia

    # Realizar la solicitud a la API y obtener la respuesta
    data = {
        "comuna": ubicacion,
        "carrera": carrera
    }
    url = "http://localhost:8081/api/v1/postulante/filtro"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()

        if isinstance(response_data, list) and len(response_data) > 0:
            response_list = []
            for postulante in response_data:
                # Crear un cuadro de texto estructurado para cada postulante
                formatted_text = f"Nombre completo: {postulante['nombres']} {postulante['apellidos']}\n"
                formatted_text += f"Correo: {postulante['email']}\n"
                formatted_text += f"Teléfono: {postulante['telefono']}\n"
                formatted_text += f"Universidad: {postulante['universidad']}"

                response_text = {
                    "text": {
                        "text": [formatted_text]
                    }
                }

                response_list.append(response_text)

            response_dict = {"fulfillmentMessages": response_list}
            return response_dict
        else:
            respuesta = formateo_respuesta(["No se encontraron postulantes con los criterios especificados."])
    else:
        respuesta = formateo_respuesta(
            ["Hubo un error al buscar en nuestra base de datos, por favor inténtalo nuevamente"])

    return respuesta

#trabajo de modelo de respaldo
async def modelo_respaldo(mensaje):
    async with SydneyClient() as sydney:
        respuesta = await  sydney.ask(mensaje)
        return respuesta
async def bing_chat(mensaje_usuario):
    async with SydneyClient() as sydney:
        while True:

            prompt =mensaje_usuario
            if prompt == '!reset':
                await sydney.reset_conversation()
                continue
            elif prompt == '!exit':
                break
            async for response in sydney.ask_stream(prompt):
                conversacion = []
                print(response)
                conversacion.append(response)
                print(conversacion)
                return conversacion
