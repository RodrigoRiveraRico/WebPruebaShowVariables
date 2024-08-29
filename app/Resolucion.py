from flask import current_app
from collections import defaultdict

def ditc_res_DBs_list(bases):
    '''
    bases : list Lista de bases de datos.

    Return : dict {'resolución1' : [DB1, DB2,], 'resolución2' : [DB1, DB3,],}
    '''
    fuente_de_datos_metadatos = current_app.config['FUENTE_DE_DATOS_METADATOS']

    psql_list = []
    endpoint_list = []
    for DB in bases:
        if fuente_de_datos_metadatos[DB]['conexion'] == 'postgresql':
            psql_list.append(DB)
        elif fuente_de_datos_metadatos[DB]['conexion'] == 'endpoints':
            endpoint_list.append(DB)

    if psql_list != []:
        from app.conexion_postgresql import resolution_from_psql
        psql_dic = resolution_from_psql(psql_list, fuente_de_datos_metadatos)

    if endpoint_list != []:
        from app.conexion_endpoints import resolution_from_endpoint
        endpoint_dic = resolution_from_endpoint(endpoint_list, fuente_de_datos_metadatos)

    if psql_list == []:
        return endpoint_dic
    elif endpoint_list == []:
        return psql_dic
    else:
        dic_union = defaultdict(list)
        for d in (psql_dic, endpoint_dic):
            for key, value in d.items():
                dic_union[key].extend(value)
        return dic_union
