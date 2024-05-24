import pandas as pd
import math

# Número de municipios en la República Mexicana
N = 2446.

# Esta función altera al DataFrame original.
# Si se quiere evitar lo anterior: hay que hacer una copia del original e indicarlo en el Return.
def df_count_cells(df_var:pd.DataFrame, df_clss:pd.DataFrame):
    '''
    df_var : pd.DataFrame variables
    df_clss : pd.DataFrame clase

    Return : None

    La función obtiene el número de celdas:
    - de las variables: N_v
    - de la intersección de cada variable con la clase: N_vnc
    '''
    df_var['N_v'] = list(map(lambda x: len(set(x)),df_var.iloc[:,-1]))  # Agrega la columna de N por variable
    df_var['N_c'] = len(list(df_clss.celdas)[0])
    df_var['N_vnc'] = [conteo_interseccion(x, list(df_clss.celdas)[0]) for x in list(df_var.celdas)] # Cuenta las intersecciones de la clase con las demás variables

    return None    # Como se modifica el DataFrame original df_var, no hace falta indicarlo en el Return.

def conteo_interseccion(l_var, l_cov):
    return sum(1 for var in l_var if var in l_cov)

def calcular_epsilon(row):
    N_c_over_N = row['N_c'] / N
    epsilon = (row['N_vnc'] - row['N_v'] * N_c_over_N) / math.sqrt(row['N_v'] * N_c_over_N * (1 - N_c_over_N))
    return epsilon

def epsilon(df_var:pd.DataFrame):
    df_var['epsilon'] = df_var.apply(calcular_epsilon, axis=1)
    return 0

def calcular_score(row):
    if row['N_v'] == row['N_vnc']:  # Evitar división por cero
        return float('inf')  # O algún valor que consideres adecuado para este caso
    return math.log(row['N_vnc'] / (row['N_v'] - row['N_vnc']))

def score(df_var:pd.DataFrame):
    df_var['Score'] = df_var.apply(calcular_score, axis=1)
    return 0