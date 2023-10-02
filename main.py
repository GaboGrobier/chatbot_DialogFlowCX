from fastapi import FastAPI , Request
from fastapi.encoders import jsonable_encoder
from rutas.formateo import formateo_respuesta
from rutas.manejador_acciones import intencion_bienvenida, intencion_postulante


app = FastAPI()

@app.post("/webhook")
async def enviarmensaje(request: Request):
    body = await request.json()
    action = body['queryResult']['action']
# Obtener los parámetros de outputContexts
    output_contexts = body.get("queryResult", {}).get("outputContexts", [])
    intencion = body.get("queryResult", {}).get("intent", {}).get("displayName")

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
