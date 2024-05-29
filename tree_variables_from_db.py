import psycopg2
import pandas as pd
from arbol_function import arbol
from config import fuente_de_datos_metadatos, query_categorias

def creacion_ramas_arbol(DB:str):
    '''
    DB : str Nombre de la base de datos
    
    Return : lst Lista para generar el árbol HTML
    '''
    conn = psycopg2.connect(database = DB,
                            user = fuente_de_datos_metadatos[DB]['user'],
                            host = fuente_de_datos_metadatos[DB]['host'],
                            password = fuente_de_datos_metadatos[DB]['password'],
                            port = fuente_de_datos_metadatos[DB]['port'])

    sql_query = query_categorias[DB]

    df = pd.read_sql(sql_query, conn)

    conn.close()

    ### https://stackoverflow.com/questions/42516616/sort-dataframe-by-string-length
    # Importante ordenar las varibales de forma ascendente al número de niveles en el que están ubicadas.
    # El diccionario (árbol) se crea guardando las variables de más internas a más externas.
    new_index = df['metadatos'].str.len().sort_values().index
    df = df.reindex(new_index)

    # df = df.head(100)   # Solo consideramos 100 datos de cada base de datos

    path_dict = arbol(df)   # Quizá un mejor nombre sería variables_categories
                            # Al usar la función arbol ya no aparecen nombres de variables repetidas, si es que las hay.

    structure_lst = []

    for path_key in path_dict.keys():   # Quizá un mejor nombre para path_key sería categorías o levels
        key_list = path_key.split(', ')
        for key_idx in range(len(key_list)):
            id_tag = DB + ' '  + ' ' + key_list[key_idx]
            if key_idx == 0:
                if structure_lst == []:
                    structure_lst.append({'id': id_tag,
                                          'text': id_tag,
                                          'children':[]})
                    idx = 0
                else:
                    for idx, d in enumerate(structure_lst):
                        if d['id'] != id_tag and idx == len(structure_lst) - 1:
                            structure_lst.append({'id': id_tag,
                                                  'text': id_tag,
                                                  'children':[]}) # Al hacer este append, añadimos una vuelta más al ciclo for         
                        elif d['id'] == id_tag:
                            break
                structure_child_lst = 'structure_lst' + str([idx]) + str(['children'])

            elif key_idx <= len(key_list) - 1:
                if eval(structure_child_lst) == []:
                    eval(structure_child_lst).append({'id': id_tag,
                                                      'text': id_tag,
                                                      'children':[]})
                    idx = 0
                else:
                    for idx, d in enumerate(eval(structure_child_lst)):
                        if d['id'] != id_tag and idx == len(eval(structure_child_lst)) - 1:
                            eval(structure_child_lst).append({'id': id_tag,
                                                              'text': id_tag,
                                                              'children':[]}) # Al hacer este append, añadimos una vuelta más al ciclo for   
                        elif d['id'] == id_tag:
                            break    
                structure_child_lst += str([idx]) + str(['children'])

        # En el siguiente append agregamos el nivel donde se almecanarán las variables.
        eval(structure_child_lst).append({'id': DB + '__variables__' + path_key,
                                          'text':'variables',
                                          'children':[]})
        # En las líneas siguientes se almacenan las variables dentro de este último diccionario creado.
        # Dado que se empleó la función 'arbol(df)' para construir el diccionario path_key, las variables a almacenar no están repetidas.

        # Queremos que el diccionario en donde se almacenarán las variables sea el primer elemento de la lista de diccionarios de structure_child_lst,
        # por eso hicimos el acomodo de  los niveles de menos profundo a más profundo.
        structure_child_lst += str([0]) + str(['children'])

        variables_lst = path_dict[path_key]['__variables__']
        
        for idx, nombre_variable in enumerate(variables_lst):
            eval(structure_child_lst).append({'id': DB + nombre_variable,
                                              'text': DB + nombre_variable,
                                              'children' : []   # Si no incuimos los intervalos, 'children' puede quedar vacío o no existir y el código subsecuente no se incluiría.  
                                              })

            last_structure_child_lst = structure_child_lst + str([idx]) + str(['children'])
            
            ser_nombre_variable = df[df['nombre_variable']==nombre_variable]['nombre_variable']
            ser_intervalo = df[df['nombre_variable']==nombre_variable]['intervalo']

            for variable_intervalo in zip(ser_nombre_variable,ser_intervalo):
                eval(last_structure_child_lst).append({'id': DB + str(variable_intervalo),
                                                       'text': DB + str(variable_intervalo[0]) + ', ' + str(variable_intervalo[1])})


    # Obtenemos lo siguiente:
    # {'id': DB + ___, 
    #  'texto': ___, 
    #  'children': [{'id': DB +'__variables__' + path_key,
    #                'text': 'variables',
    #                'children' : [{'id': DB + ___,
    #                               'text': nombre_variable,
    #                               'children':[{'id': DB + ___,
    #                                            'texto': nombre_variable + intervalo},]
    #                             },]
    #                 },
    #                 {'id': DB + ___,
    #                     'text': ___,
    #                     'children': []},
    #             ], 
    # }

    return structure_lst