from rutas.formateo import formateo_respuesta
from decouple import config
from hugchat import hugchat
from hugchat.login import Login
import requests
import json


#configuracion intencion de bienvenida
def intencion_bienvenida(body : dict)->dict :
    #session = body['session']
    #print('esta es la session',session)
    #return session


    respuesta = formateo_respuesta(
        [
            'Hola seré tu asistente de TalentQuest ',
            'Necesito que me indiques minimo 1 carrera y region de donde buscas tus candidatos ',

        ]
    )
    return respuesta

#configuracion accion para intencion de solicitud de postulante
def intencion_postulante(carrera, region):
    #Inicializar las variables
    ubicacion = region
    estado = None
    carrera = carrera
    cantidad = None


    # Realizar la solicitud a la API y obtener la respuesta
    data = {
        "comuna": ubicacion,
        "carrera": carrera
    }
    url = "http://54.237.232.232:8081/api/v1/postulante/filtro"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()

        if isinstance(response_data, list) and len(response_data) > 0:
            response_list = []
            for postulante in response_data:
                # Crear un mensaje de texto para cada postulante
                formatted_text = f"Nombre completo: {postulante['nombres']} {postulante['apellidos']}\n"
                formatted_text += f"Correo: {postulante['email']}\n"
                formatted_text += f"Teléfono: {postulante['telefono']}\n"
                formatted_text += f"Universidad: {postulante['universidad']}"

                # Agregar un separador entre los resultados
                formatted_text += "\n___________________\n"

                text_response = {
                    "text": {
                        "text": [formatted_text]
                    }
                }

                response_list.append(text_response)

            # Formatear la respuesta de acuerdo con el formato de Dialogflow CX
            fulfillment_response = {"fulfillment_response": {"messages": response_list}}
            return fulfillment_response









def interactuar_con_hugchat(mensaje_usuario):
    sign = Login(config('User_hug'), config('passhug'))
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies)
    id_conversacion = chatbot.new_conversation()
    chatbot.switch_llm(0)

    respuesta_hugchat = chatbot.chat(mensaje_usuario)
    return respuesta_hugchat


def interactuar_con_hugchat(mensaje_usuario):
    sign = Login(config('User_hug'), config('passhug'))
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies)
    id_conversacion = chatbot.new_conversation()
    chatbot.switch_llm(0)

    respuesta_hugchat = chatbot.chat(mensaje_usuario)
    return respuesta_hugchat




