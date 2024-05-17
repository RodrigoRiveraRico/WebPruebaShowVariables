import psycopg2
import pandas as pd
from arbol_function import arbol
from config import fuente_de_datos_metadatos

def creacion_ramas_arbol():

    db = 'epi_puma_censo_inegi_2020'
    conn = psycopg2.connect(database = fuente_de_datos_metadatos[db]['database'],
                            user = fuente_de_datos_metadatos[db]['user'],
                            host = fuente_de_datos_metadatos[db]['host'],
                            password = fuente_de_datos_metadatos[db]['password'],
                            port = fuente_de_datos_metadatos[db]['port'])

    sql_query = '''
        select case
        when name like 'Grado promedio%' then name
        when name like '%afiliada%servicios%' then name
        when name like '%condici_n mental%' or name like '%discapacidad%' or name like '%limitaci_n%' then name
        when name like '%censales%referencia%' or name like '%viviendas particulares%' or name like '%religi_n%' or name like '%a_os%' or name like '%poblaci_n nacida%entidad%' then name
        when name like '%poblaci_n femeninca%' or name like '%pobalci_n masculina' then name
        when name like '%viviendas particulares%' then name
        when name like '%viviendas particulares habitadas que no%' then name
        else name 
    end as nombre_variable,

    interval as intervalo,

    case 
        when name like 'Grado promedio%' then concat('estudios',', ','escolaridad') 
        when name like '%afiliada%servicios%' then concat('salud',', ','servicios salud')
        when name like '%condici_n mental%' or name like '%discapacidad%' or name like '%limitaci_n%' then concat('salud',', ','discapacidad')
        when name like '%censales%referencia%' or name like '%viviendas particulares%' or name like '%religi_n%' or name like '%a_os%' or name like '%poblaci_n nacida%entidad%' then concat('personas',', ','población')
        when name like '%poblaci_n femeninca%' or name like '%pobalci_n masculina' then concat('personas',', ','genero')
        when name like '%viviendas particulares%' then concat('vivienda',', ','vivienda1')
        when name like '%viviendas particulares habitadas que no%' then concat('vivienda',', ','vivienda2')
        else concat('categoria1')
    end as metadatos

    from covariable
    ;
    '''

    df = pd.read_sql(sql_query, conn)

    conn.close()

    ### https://stackoverflow.com/questions/42516616/sort-dataframe-by-string-length
    # Importante ordenar las varibales de forma ascendente al número de niveles en el que están ubicadas.
    # El diccionario (árbol) se crea guardando las variables de más internas a más externas.
    new_index = df['metadatos'].str.len().sort_values().index
    df = df.reindex(new_index)

    df_prueba = df#.head(10)
    # print(arbol(df_prueba))
    # print(df_prueba.to_string())

    # https://stackoverflow.com/questions/33898929/create-jstree-hierarchy-from-parent-child-pair-from-table


    path_dict = arbol(df_prueba)    # Quizá un mejor nombre sería variables_categories

    structure_lst = []

    lst_prueba = ['personas, poblacion, algo1', 'salud', 'estudios, escolaridad', 'salud, discapacidad', 'categoria1, categoria2, categoria3']

    for path_key in path_dict.keys():   # Quizá un mejor nombre para path_key sería categoría o level
    # for path_key in lst_prueba:
        key_list = path_key.split(', ')
        # print(key_list)
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
                # print(structure_child_lst, key_list[key_idx])

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
                # print(structure_child_lst, key_list[key_idx])

        print('\n')
        # En el siguiente append agregamos el nivel donde se almecanarán las variables.
        eval(structure_child_lst).append({'id':'__variables__',
                                        'text':'variables',
                                        'children':[]})
        # Ahora a hacer un ciclo for para almacenar las variables :D
        # Valdría la pena revisar si la variable a almacenar ya está incluida


        # Queremos que la estructura de variables sea el primer elemento
        # para ello requerimos acomodar los niveles de menos profundo a más profundo
        structure_child_lst += str([0]) + str(['children'])

        # print(path_key)
        variables_lst = path_dict[path_key]['__variables__']
        # print(variables_lst)
        
        for idx, nombre_variable in enumerate(variables_lst):
            eval(structure_child_lst).append({'id': '*',    # Quiza este 'id' podría ser solo un número o clave
                                            'text': nombre_variable,
                                            'children' : []   # Si no incuimos los intervalos, 'children' puede quedar vacío o no existir   
                                            })

            last_structure_child_lst = structure_child_lst + str([idx]) + str(['children'])
            
            ser_nombre_variable = df_prueba[df_prueba['nombre_variable']==nombre_variable]['nombre_variable']
            ser_intervalo = df_prueba[df_prueba['nombre_variable']==nombre_variable]['intervalo']

            for variable_intervalo in zip(ser_nombre_variable,ser_intervalo):
                eval(last_structure_child_lst).append({'id': '#',
                                                    'text': str(variable_intervalo[0]) + ', ' + str(variable_intervalo[1])})


    # Hasta este punto tenemos:
    # {'id': ___, 
    #  'texto': ___, 
    #  'children': [{'id': '__variables__',
    #                'text': 'variables',
    #                'children' : [{'id': ___,
    #                               'text': ___}]},
    #                 {'id': ___,
    #                  'text': ___,
    #                  'children': []}], 
    # }


    # print(structure_lst)

    return structure_lst

# print(creacion_ramas_arbol())