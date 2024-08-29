from flask import current_app

def creacion_ramas_arbol(DB: str):
    '''
    DB: str Nombre de la fuente de datos (base de datos).
    
    Return: list Lista para generar el árbol HTML
    '''
    fuente_de_datos_metadatos = current_app.config['FUENTE_DE_DATOS_METADATOS']
    query_categorias = current_app.config['QUERY_CATEGORIAS']
    conexion = fuente_de_datos_metadatos[DB]['conexion']

    if conexion == 'postgresql':
        from app.conexion_postgresql import tree_from_psql
    elif conexion == 'endpoints':
        from app.conexion_endpoints import tree_from_endpoint

    if conexion == 'postgresql':
        df = tree_from_psql(DB, fuente_de_datos_metadatos, query_categorias)
    elif conexion == 'endpoints':
        df = tree_from_endpoint(DB, fuente_de_datos_metadatos)
    # print(df)

    # Crear una nueva columna con una lista de la taxonomía de la variable
    df['taxonomia_variable_lst'] = df['taxonomia_variable'].str.split(r"_-_", expand=False, regex=False)

    # Ordenar el DataFrame
    df = df.sort_values(
        by=['metadatos', 'taxonomia_variable']  # Ordenar primero por 'metadatos'.
        )

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

    return structure_lst
    # return structure_lst[0]['children'] # Regresamos este 'children' para no mostrar dos veces el nombre de la base de datos en el árbol
                                        # Esto elimmina las categorías de postgres INEGI

    

# Ejemplo de uso
# creacion_ramas_arbol('Personas')
# creacion_ramas_arbol('epi_puma_worldclim')
