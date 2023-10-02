def formateo_respuesta(mensaje: list[str]):
    respuesta_data = {"fulfillmentMessages": []}
    for mensajes in mensaje:
        respuesta_data['fulfillmentMessages'].append(
            {
                    "text": {
                        "text": [mensajes]
                    }
            }
        )
    return respuesta_data