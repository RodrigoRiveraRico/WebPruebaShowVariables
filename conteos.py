import pandas as pd

# Esta función altera al DataFrame original.
# Si se quiere evitar lo anterior: hay que hacer una copia del original e indicarlo en el Return.
def df_count_cells(df_var:pd.DataFrame, df_clss:pd.DataFrame):
    '''
    df_var : pd.DataFrame variables
    df_clss : pd.DataFrame clase

    Return : None
    '''
    df_var['N_v'] = list(map(lambda x: len(set(x)),df_var.iloc[:,-1]))  # Agrega la columna de N por variable
    df_var['N_vnc'] = [conteo_interseccion(x, list(df_clss.celdas)[0]) for x in list(df_var.celdas)] # Cuenta las intersecciones de la clase con las demás variables

    return None    # Como se modifica el DataFrame original df_var, no hace falta indicarlo en el Return.

def conteo_interseccion(l_var, l_cov):
    return sum(1 for var in l_var if var in l_cov)