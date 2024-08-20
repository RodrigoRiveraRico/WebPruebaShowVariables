import pandas as pd
from flask import current_app
from sqlalchemy import create_engine, text

# Función para contar el número de elementos separados por coma
def count_elements(metadata):
    '''
    La columna 'metadatos' tiene a las categorías separadas por coma.
    Categorías más internas tienen más elementos.
    Categorías menos internas tienen menos elementos.
    '''
    return len(metadata.split(','))

def creacion_ramas_arbol(DB: str):
    '''
    DB : str Nombre de la base de datos
    
    Return : lst Lista para generar el árbol HTML
    '''
    def conexion_psql():
        '''
        Función que hace la conexión a postgresql.

        Return : DataFrame
        '''
        fuente_de_datos_metadatos = current_app.config['FUENTE_DE_DATOS_METADATOS']
        query_categorias = current_app.config['QUERY_CATEGORIAS']
        user = fuente_de_datos_metadatos[DB]['user']
        host = fuente_de_datos_metadatos[DB]['host']
        password = fuente_de_datos_metadatos[DB]['password']
        port = fuente_de_datos_metadatos[DB]['port']
        database = DB
        database_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

        engine = create_engine(database_url)

        sql_query = text(query_categorias[DB])

        with engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)

        return df
    
    def conexion_endpoint():
        import requests
        fuente_de_datos_metadatos = current_app.config['FUENTE_DE_DATOS_METADATOS']
        api_url = fuente_de_datos_metadatos[DB]['variables']
        response = requests.get(api_url).json()
        df_response = pd.json_normalize(response)
        df_response.rename(columns={'name':'taxonomia_variable'}, inplace=True)
        df_response['metadatos'] = DB   # Aparecerá 2 veces el nombre de la base en el árbol
        df = df_response[['id', 'taxonomia_variable', 'metadatos']]
        return df

    df = conexion_endpoint()
    # print(df)

    # df = conexion_psql()
    # print(df)
    # Crear una nueva columna temporal con el conteo de elementos.
    df['element_count'] = df['metadatos'].apply(count_elements)

    # Crear una nueva columna con una lista de la taxonomía de la variable
    df['taxonomia_variable_lst'] = df['taxonomia_variable'].str.split(r"_-_", expand=False, regex=False)

    # Ordenar el DataFrame
    df = df.sort_values(
        by=['element_count', 'metadatos', 'taxonomia_variable']  # Ordenar primero por 'element_count'.
        ).drop(columns=['element_count'])  # Eliminar la columna temporal después de ordenar.
    # print(df)

    structure_lst = []

    def add_node(id_tag, text, children_list):
        return {'id': id_tag, 'text': text, 'children': children_list}

    def find_or_create_node(structure, id_tag, text):
        for node in structure:
            if node['id'] == id_tag:
                return node
        new_node = add_node(id_tag, text, [])
        structure.append(new_node)
        return new_node
    
    for path in df.metadatos.unique():
        path_list = [x.strip() for x in path.split(',')]
        id_tag = DB + ' '
        current_structure = structure_lst

        for level in path_list:
            id_tag += level + ' '
            node = find_or_create_node(current_structure, id_tag, level)
            current_structure = node['children']

        # Agregar nodo de variables
        variables_node = add_node(DB + '__variables__' + path, 'variables', [])
        current_structure.append(variables_node)

        # Agregar variables dentro del nodo de variables
        var_tax_lst_ser = df[df['metadatos']==path]['taxonomia_variable_lst']
        var_tax_idx_ser = df[df['metadatos']==path]['id']

        for var_tax_idx, var_tax_lst in zip(var_tax_idx_ser, var_tax_lst_ser):
            var_tax_string = ''
            id_tag = DB + ' ' + path + ' '
            current_structure = variables_node['children']
            for idx, var_tax in enumerate(var_tax_lst):
                if idx == len(var_tax_lst) - 1:
                    id_tag = '__' + DB + '__ ' + path + ' __' + str(var_tax_idx)  + '__'
                else:
                    id_tag += var_tax + ', '
                var_tax_string += var_tax + ', '
                node = find_or_create_node(current_structure, id_tag, var_tax_string[:-2])
                current_structure = node['children']

    return structure_lst[0]['children'] # Regresamos este 'children' para no mostrar dos veces el nombre de la base de datos en el árbol

    

# Ejemplo de uso
# creacion_ramas_arbol('Personas')
# creacion_ramas_arbol('epi_puma_worldclim')
