import pandas as pd
from flask import current_app
from sqlalchemy import create_engine, text

# Esta función tiene como objetivo devolver una lista con las celdas
# donde las variables seleccionadas tienen presencia.
# Nota: una lista de celdas por cada base de datos.
def recolectar_celdas(DB:str, variables:list, res:str):
    fuente_de_datos_metadatos = current_app.config['FUENTE_DE_DATOS_METADATOS']
    user = fuente_de_datos_metadatos[DB]['user']
    host = fuente_de_datos_metadatos[DB]['host']
    password = fuente_de_datos_metadatos[DB]['password']
    port = fuente_de_datos_metadatos[DB]['port']
    database = DB
    database_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

    engine = create_engine(database_url)
    
    # Columna donde están almacenadas las celdas
    col_cells = fuente_de_datos_metadatos[DB]['resolution'][res]

    # Columna donde están almacenadas los nombres de las variables
    # col_names = fuente_de_datos_metadatos[DB]['lab_var'][0]

    # Columna donde están almacenados los intervalos de las variables
    # col_interval = fuente_de_datos_metadatos[DB]['lab_var'][1]

    var_cols = fuente_de_datos_metadatos[DB]['lab_var']

    # Nombre de la tabla
    table = fuente_de_datos_metadatos[DB]['table']

    str_ = ",', ',".join(var_cols)
    str_2 = ", ".join(var_cols)

    # Consulta
    sql_query = text(f'''
        with data as (
            select concat({str_}) as variable,
            {col_cells},
            {str_2}
            from {table}
            )
        select variable, {col_cells} 
        from data 
        where variable in :variables;
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

# Ejemplo de uso
# variables = ['Annual Mean Temperature, 13.525:15.225', 'Annual Mean Temperature, 15.225:16.146', ...]
# recolectar_celdas('Personas', variables, 'UNAM_1057')
# recolectar_celdas('epi_puma_worldclim', variables, 'mun')