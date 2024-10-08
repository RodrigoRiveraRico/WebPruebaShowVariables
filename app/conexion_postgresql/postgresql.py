import pandas as pd
import configuraciones_db.sql_config_construction as sql_c
from sqlalchemy import create_engine, text

def resolution_from_psql(bases, fuente_de_datos_metadatos):
    '''
    Función que se emplea con la configuración para conectar bases de datos en postgresql.

    Return: Diccionario.
    '''
    dic = {}    # Diccionario a construir.
    for db in bases:    # Para cada base de las seleccionadas
        res_dict = fuente_de_datos_metadatos[db]['resolution']  # Se asigna el diccionario de resolucion de cada base
        for key in res_dict.keys(): # Cada key es una resolución
            if key not in dic:  # Si la resolucion no está en el diccionario
                dic.update({key:[]})    # Agregamos la resolución faltante cuyos valores será una lista de bases de datos
            dic[key].append(db) # Añadimos la base de datos a la resolución
    return dic

def tree_from_psql(DB: str, fuente_de_datos_metadatos: dict, res: str):
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

    def sql_query():
        db_config_values = fuente_de_datos_metadatos[DB]

        if db_config_values['categorias'] == None:
            metadatos_txt = f"""'"{DB}"'"""

        elif "archivo" in db_config_values['categorias']:
            archivo_name = db_config_values['categorias']['archivo'][:-3]
            exec(f"import configuraciones_db.{archivo_name} as sql_txt")
            metadatos_txt = eval('sql_txt.txt')

        elif "columnas" in db_config_values['categorias']:
            metadatos_txt = f'CONCAT({sql_c.concatenacion_metadatos(db_config_values)})'

        txt = f"""
                SELECT 
                    {db_config_values['id_column']} as id,
                    
                    CONCAT({sql_c.concatenacion_taxonomia(db_config_values)}) as taxonomia_variable,

                    {metadatos_txt} as metadatos

                FROM {sql_c.table(db_config_values)}

                WHERE {db_config_values['resolution'][res]} IS NOT NULL
                ;
                """
        
        return text(txt)

    sql_query = sql_query()

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
