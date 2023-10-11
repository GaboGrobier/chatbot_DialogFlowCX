from rutas.formateo import formateo_respuesta
def intencion_bienvenida(body : dict)->dict :
    session = body['session']
    print('esta es la session',session)

    respuesta = formateo_respuesta(
        [
            'Hola seré tu asistente de TalentQuest ',
            'Necesito que me indiques minimo 1 carrera y region de donde buscas tus candidatos ',

        ]
    )
    return respuesta
def intencion_postulante(body: dict)->dict:
    # Obtener los parámetros de outputContexts
    output_contexts = body.get("queryResult", {}).get("outputContexts", [])

    # Inicializar las variables
    ubicacion = None
    estado = None
    carrera = None
    cantidad = None

    # Iterar sobre los contextos y obtener los parámetros
    for context in output_contexts:
        parametros = context.get("parameters", {})
        ubicacion = parametros.get("Ubicacion") or ubicacion
        estado = parametros.get("Estado") or estado
        carrera = parametros.get("Carrera") or carrera
        cantidad = parametros.get("cantidad") or cantidad
    respuesta = formateo_respuesta(
        [
           'Entedemos, dejanos buscar en nuestra Base datos',
            'Estamos buscando un postulante de la carrera de :', carrera,
            f'y que este en la region de :',ubicacion
        ]
    )
    return respuesta
