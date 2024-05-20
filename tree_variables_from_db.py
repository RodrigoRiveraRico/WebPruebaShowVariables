import psycopg2
import pandas as pd
from arbol_function import arbol
from config import fuente_de_datos_metadatos, query_categorias

def creacion_ramas_arbol(DB:str):
    '''
    DB : str Nombre de la base de datos
    
    Return : lst Lista para generar el árbol HTML
    '''
    conn = psycopg2.connect(database = fuente_de_datos_metadatos[DB]['database'],
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

    path_dict = arbol(df)   # Quizá un mejor nombre sería variables_categories
                            # Al usar la función arbol ya no aparecen nombres de variables repetidas

    structure_lst = []

    for path_key in path_dict.keys():   # Quizá un mejor nombre para path_key sería categoría o level
        key_list = path_key.split(', ')
        for key_idx in range(len(key_list)):
            if key_idx == 0:
                if structure_lst == []:
                    structure_lst.append({'id': key_list[key_idx],
                                        'text': key_list[key_idx],
                                        'children':[]})
                    idx = 0
                else:
                    for idx, d in enumerate(structure_lst):
                        if d['id'] != key_list[key_idx] and idx == len(structure_lst) - 1:
                            structure_lst.append({'id': key_list[key_idx],
                                                'text': key_list[key_idx],
                                                'children':[]}) # Al hacer este append, añadimos una vuelta más al ciclo for         
                        elif d['id'] == key_list[key_idx]:
                            break
                structure_child_lst = 'structure_lst' + str([idx]) + str(['children'])

            elif key_idx <= len(key_list) - 1:
                if eval(structure_child_lst) == []:
                    eval(structure_child_lst).append({'id': key_list[key_idx],
                                                'text': key_list[key_idx],
                                                'children':[]})
                    idx = 0
                else:
                    for idx, d in enumerate(eval(structure_child_lst)):
                        if d['id'] != key_list[key_idx] and idx == len(eval(structure_child_lst)) - 1:
                            eval(structure_child_lst).append({'id': key_list[key_idx],
                                                            'text': key_list[key_idx],
                                                            'children':[]}) # Al hacer este append, añadimos una vuelta más al ciclo for   
                        elif d['id'] == key_list[key_idx]:
                            break    
                structure_child_lst += str([idx]) + str(['children'])

        # En el siguiente append agregamos el nivel donde se almecanarán las variables.
        eval(structure_child_lst).append({'id':'__variables__',
                                        'text':'variables',
                                        'children':[]})
        # Ahora a hacer un ciclo for para almacenar las variables :D
        # Valdría la pena revisar si la variable a almacenar ya está incluida


        # Queremos que la estructura de variables sea el primer elemento
        # por eso hicimos el acomodo de  los niveles de menos profundo a más profundo
        structure_child_lst += str([0]) + str(['children'])

        variables_lst = path_dict[path_key]['__variables__']
        
        for idx, nombre_variable in enumerate(variables_lst):
            eval(structure_child_lst).append({'id': nombre_variable,    # Quiza este 'id' podría ser solo un número o clave
                                            'text': nombre_variable,
                                            'children' : []   # Si no incuimos los intervalos, 'children' puede quedar vacío o no existir   
                                            })

            last_structure_child_lst = structure_child_lst + str([idx]) + str(['children'])
            
            ser_nombre_variable = df[df['nombre_variable']==nombre_variable]['nombre_variable']
            ser_intervalo = df[df['nombre_variable']==nombre_variable]['intervalo']

            for variable_intervalo in zip(ser_nombre_variable,ser_intervalo):
                eval(last_structure_child_lst).append({'id': str(variable_intervalo),
                                                    'text': str(variable_intervalo[0]) + ', ' + str(variable_intervalo[1])})


    # Obtenemos lo siguiente:
    # {'id': ___, 
    #  'texto': ___, 
    #  'children': [{'id': '__variables__',
    #                'text': 'variables',
    #                'children' : [{'id': ___,
    #                               'text': nombre_variable,
    #                               'children':[{'id': ___,
    #                                            'texto': nombre_variable + intervalo},]
    #                             },]
    #                 },
    #                 {'id': ___,
    #                     'text': ___,
    #                     'children': []},
    #             ], 
    # }

    return structure_lst