from flask import current_app

def recolectar_celdas(DB:str, variables:list, res:str):
    '''
    Función que obtiene, para cada variable, la lista de celdas donde hay presencia de estas.
    DB: str Nombre de la fuente de datos.
    variables: list Lista de variables.
    res: str Resolución.

    Return: Resultado de la función conexion_psql o de la función conexion_endpoint.
    NOTA: Ambas funciones regresan una tupla de arreglos numpy.
    '''
    fuente_de_datos_metadatos = current_app.config['FUENTE_DE_DATOS_METADATOS']
    conexion = current_app.config['CONEXION']

    if conexion == 'postgresql':
        from app.conexion_postgresql import cells_from_psql
    elif conexion == 'endpoints':
        from app.conexion_endpoints import cells_from_endpoint

    if conexion == 'postgresql':
        return cells_from_psql(DB, variables, res, fuente_de_datos_metadatos)
    elif conexion == 'endpoints':
        return cells_from_endpoint(DB, variables, res, fuente_de_datos_metadatos)


# Ejemplo de uso (con conexion_psql())
# variables = ['Annual Mean Temperature, 13.525:15.225', 'Annual Mean Temperature, 15.225:16.146', ...]
# recolectar_celdas('Personas', variables, 'UNAM_1057')
# recolectar_celdas('epi_puma_worldclim', variables, 'mun')