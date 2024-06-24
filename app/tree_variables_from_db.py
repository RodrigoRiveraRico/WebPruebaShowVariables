import pandas as pd
from app.arbol_function import arbol
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

    # Crear una nueva columna temporal con el conteo de elementos.
    df['element_count'] = df['metadatos'].apply(count_elements)

    df_taxonomia_variables = df['taxonomia_variable'].str.split(r"_-_", expand=True)
    for i in df_taxonomia_variables:
        df['var_tax_'+str(i)] = df_taxonomia_variables[i]

    # Ordenar el DataFrame
    df = df.sort_values(
        by=['element_count', 'metadatos', 'taxonomia_variable', 'intervalo']  # Ordenar primero por 'element_count'.
    ).drop(columns=['element_count'])  # Eliminar la columna temporal después de ordenar.
    print(df)

    # path_dict = arbol(df)

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

    for path_key in df.metadatos.unique():
        value = df[df['metadatos'] == path_key]['var_tax_0'].unique()   # Esta línea ya no iría.
        key_list = path_key.split(', ')
        id_tag = DB + ' '
        current_structure = structure_lst
  
    # for path_key, value in path_dict.items():
    #     key_list = path_key.split(', ')
    #     id_tag = DB + ' '
    #     current_structure = structure_lst

        for key_idx, key in enumerate(key_list):
            id_tag += key + ' '
            node = find_or_create_node(current_structure, id_tag, key)
            current_structure = node['children']

        # Agregar nodo de variables
        variables_node = add_node(DB + '__variables__' + path_key, 'variables', [])
        current_structure.append(variables_node)

        # Agregar variables dentro del nodo de variables
        for var_tax_0 in value: # value_lst = df[df['metadatos'] == path_key]['taxonomia_variable'] y aplicamos de forma análoga la creación de nodos de arriba.
            variable_node = add_node(DB + ' ' + path_key + ' ' + var_tax_0, var_tax_0, [])
            variables_node['children'].append(variable_node)

            ser_nombre_variable = df[(df['var_tax_0'] == var_tax_0) & (df['metadatos'] == path_key)]['var_tax_0']
            ser_intervalo = df[(df['var_tax_0'] == var_tax_0) & (df['metadatos'] == path_key)]['var_tax_1']

            for variable_intervalo in zip(ser_nombre_variable, ser_intervalo):
                interval_node = add_node('__' + DB + '__' + ' ' + path_key + ' ' + str(variable_intervalo),
                                         str(variable_intervalo[0]) + ', ' + str(variable_intervalo[1]), [])
                variable_node['children'].append(interval_node)

    return structure_lst

    

# Ejemplo de uso
# creacion_ramas_arbol('Personas')
# creacion_ramas_arbol('epi_puma_worldclim')
