import pandas as pd
from sqlalchemy import create_engine, text

def tree_from_psql(DB: str, fuente_de_datos_metadatos: dict, query_categorias):
    '''
    Función que se emplea con la configuración para conectar bases de datos en postgresql.
    Esta función hace la conexión a postgresql.

    Return : DataFrame
    '''
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

    return df

def cells_from_psql(DB: str, variables: list, res: str, fuente_de_datos_metadatos: dict):
    '''
    Función que se emplea con la configuración para conectar bases de datos en postgresql.
    Esta función hace la conexión a postgresql.
    

    Return : Tupla de arreglos numpy
    '''
    user = fuente_de_datos_metadatos[DB]['user']
    host = fuente_de_datos_metadatos[DB]['host']
    password = fuente_de_datos_metadatos[DB]['password']
    port = fuente_de_datos_metadatos[DB]['port']
    database = DB
    database_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

    engine = create_engine(database_url)
    
    # Columna donde están almacenadas las celdas
    col_cells = fuente_de_datos_metadatos[DB]['resolution'][res]

    # Lista de columnas donde está almacenada la taxonomía de las variables.
    tax_var_cols = fuente_de_datos_metadatos[DB]['variable_columns']

    # String que une la taxonomía de las variables
    columnas_variable = ",', ',".join(tax_var_cols)

    # Nombre de la tabla
    table = fuente_de_datos_metadatos[DB]['table']

    # Columna de id's
    id_column = fuente_de_datos_metadatos[DB]['id_column']

    # Consulta
    sql_query = text(f'''
        WITH data AS (
            SELECT {id_column} AS id_variable,
            CONCAT({columnas_variable}) AS variable,
            {col_cells}
            FROM {table}
            )
        SELECT id_variable, variable, {col_cells} 
        FROM data 
        WHERE id_variable IN :variables;
        ''')

    # Convertir la lista de variables a una tupla
    variables_tuple = tuple(variables)

    # Imprimir la consulta SQL y los parámetros
    # print("Consulta SQL:", sql_query)
    # print("Parámetros:", {'variables': variables_tuple})

    # Ejecutar la consulta y leer los resultados en un DataFrame
    with engine.connect() as connection:
        df = pd.read_sql(sql_query, connection, params={'variables': variables_tuple}) # Cada registro del df es una lista de celdas
        
    df[col_cells] = df[col_cells].astype(str)   # Aseguramos que la columna de celdas sea un string
    df[col_cells] = df[col_cells].str.findall(r'\d+') # Con findall obtenemos una lista de strings
    # print(df)

    return df['variable'].to_numpy(), df[col_cells].to_numpy()
