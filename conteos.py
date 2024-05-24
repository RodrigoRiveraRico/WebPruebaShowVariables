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
    - de la clase: N_c
    - de la intersección de cada variable con la clase: N_vnc
    '''
    df_var['N_v'] = list(map(lambda x: len(set(x)),df_var.iloc[:,-1]))  # Número de celdas de cada variable.
    df_var['N_c'] = len(list(df_clss.celdas)[0])    # Número de celdas de la clase.
    df_var['N_vnc'] = [conteo_interseccion(x, list(df_clss.celdas)[0]) for x in list(df_var.celdas)] # Cuenta las intersecciones de la clase con las demás variables
    
    # Como se modifica el DataFrame original df_var, no hace falta indicarlo en el Return.
    return None

def conteo_interseccion(l_var, l_clss):
    '''
    Cuenta las celdas en la intersección entre variables y clase.
    '''
    return sum(1 for var in l_var if var in l_clss)

def calcular_epsilon(row):
    '''
    Función que se aplicará a cada fila del DataFrame para calcular el epsilon.
    '''
    N_c_over_N = row['N_c'] / N
    epsilon = (row['N_vnc'] - row['N_v'] * N_c_over_N) / math.sqrt(row['N_v'] * N_c_over_N * (1 - N_c_over_N))
    return round(epsilon,2)

def epsilon(df_var:pd.DataFrame):
    '''
    Aplica la función 'calcular_epsilon' a cada fila del DataFrame.
    Se modifica el DataFrame original, por lo que se regresa None.
    '''
    df_var['epsilon'] = df_var.apply(calcular_epsilon, axis=1)
    return None

def calcular_score(row):
    '''
    Función que se aplicará a cada fila del DataFrame para calcular el score.
    '''
    if row['N_v'] == row['N_vnc'] or row['N_vnc'] == 0:  # Evitar división por cero o que el argumento de log sea cero.
        return float('inf')  # O algún valor que se considere adecuado para este caso.
    score = math.log(row['N_vnc'] / (row['N_v'] - row['N_vnc']))
    return round(score,2)

def score(df_var:pd.DataFrame):
    '''
    Aplica la función 'calcular_score' a cada fila del DataFrame.
    Se modifica el DataFrame original, por lo que se regresa None.
    '''
    df_var['score'] = df_var.apply(calcular_score, axis=1)
    return None