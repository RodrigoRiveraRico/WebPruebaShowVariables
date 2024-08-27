from flask import current_app

def ditc_res_DBs_list(bases):
    '''
    bases : list Lista de bases de datos.

    Return : dict {'resolución1' : [DB1, DB2,], 'resolución2' : [DB1, DB3,],}
    '''
    fuente_de_datos_metadatos = current_app.config['FUENTE_DE_DATOS_METADATOS']
    conexion = current_app.config['CONEXION']

    if conexion == 'postgresql':
        from app.conexion_postgresql import resolution_from_psql
    elif conexion == 'endpoints':
        from app.conexion_endpoints import resolution_from_endpoint

    if conexion == 'postgresql':
        return resolution_from_psql(bases, fuente_de_datos_metadatos)
    elif conexion == 'endpoints':
        return resolution_from_endpoint(bases, fuente_de_datos_metadatos)
