#formateo de texto para poder ser enviado a traves de dialogflow

def formateo_respuesta(mensaje: list[str]):
    respuesta_data = {
        "fulfillment_response": {
            "messages": []
        }
    }

    for mensaje_texto in mensaje:
        respuesta_data["fulfillment_response"]["messages"].append(
            {
                "text": {
                    "text": [mensaje_texto]
                }
            }
        )

    return respuesta_data