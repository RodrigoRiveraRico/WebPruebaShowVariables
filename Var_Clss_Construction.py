import pandas as pd
import numpy as np
from arbol_function import arbol
from PyPostQL import retrieve_cells

def dict_construction(list_db_var:list):
    '''
    list_dv_var : list

    Return : dict
    '''
    db_list = []
    var_list = []

    for pair_db_var in list_db_var:
        aux_index = pair_db_var.find(':')
        db_list.append(pair_db_var[0:aux_index])
        var_list.append(pair_db_var[aux_index+1:])

    data = {
        'nombre_variable': var_list,
        'metadatos': db_list
    }

    df = pd.DataFrame(data)

    return arbol(df)



def df_construction(dict_db_var:dict, column_name:str, res:str):
    '''
    dict_db_var : dict
    column_name : str 
                Nombre de la columna del DataFrame resultante.
    res : str
        Resolución del ensamble.

    Return : pandas DataFrame
    '''
    variables_array = np.array([])
    cells_array = np.array([])

    for db_name in dict_db_var:
        variables = dict_db_var[db_name]['__variables__']     # Esto es una lista
        
        # Queremos que variables tenga estructura ('_nombre_variable_1', 'nombre_variables_2') para la consulta SQL
        if len(variables) == 1:
            variables = "('" + str(variables[0]) + "')"

        else:
            variables = str(tuple(variables))

        array_1, array_2 = retrieve_cells.recolectar_celdas(db_name, variables, res)
        
        variables_array = np.append(variables_array, array_1)
        cells_array = np.append(cells_array, array_2)

    # DataFrame con todas las variables seleccionadas    
    return pd.DataFrame({column_name : variables_array,
                        'celdas' : cells_array})