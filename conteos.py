import pandas as pd

# Modificar esta función para crear una copia del DataFrame original
# y no alterar el original.
# Revisar si es necesario el return de la función. <- No es necesario el return de la función
# si lo que se quiere es alterar el DataFrame original.
def df_count_cells(df_var:pd.DataFrame, df_clss:pd.DataFrame):
    '''
    df_var : pd.DataFrame variables
    df_clss : pd.DataFrame clase

    Return : pd.DataFrame de las variables
    '''
    df_var['N_v'] = list(map(lambda x: len(set(x)),df_var.iloc[:,-1]))  # Agrega la columna de N por variable
    df_var['N_vnc'] = [conteo_interseccion(x, list(df_clss.celdas)[0]) for x in list(df_var.celdas)] # Cuenta las intersecciones de la clase con las demás variables

    return df_var

def conteo_interseccion(l_var, l_cov):
    return sum(1 for var in l_var if var in l_cov)