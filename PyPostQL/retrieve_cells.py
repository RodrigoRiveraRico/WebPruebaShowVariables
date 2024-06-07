import psycopg2
import pandas as pd
from config import fuente_de_datos_metadatos

# Esta función tiene como objetivo devolver una lista con las celdas
# donde las variables seleccionadas tienen presencia.
# Nota: una lista de celdas por cada base de datos.
def recolectar_celdas(DB:str, variables:str, res:str):
    conn = psycopg2.connect(database = DB, 
                            user = fuente_de_datos_metadatos[DB]['user'], 
                            host= fuente_de_datos_metadatos[DB]['host'],
                            password = fuente_de_datos_metadatos[DB]['password'],
                            port = fuente_de_datos_metadatos[DB]['port']
                            )
    
    # Columna donde están almacenadas las celdas
    col_cells = fuente_de_datos_metadatos[DB]['resolution'][res]

    # Columna donde están almacenadas los nombres de las variables
    col_names = fuente_de_datos_metadatos[DB]['lab_var']

    # Columna donde están almacenados los intervalos de las variables
    col_interval = fuente_de_datos_metadatos[DB]['interval']

    # Nombre de la tabla
    table = fuente_de_datos_metadatos[DB]['table']

    # Consulta
    sql_query = '''
    with data as (
        select concat({0},', ',{1}) as variable,
        {2},
        {0},
        {1}
        from {3}
        )
    select variable, {2} 
    from data 
    where variable in {4};
    '''.format(col_names, col_interval, col_cells, table, variables)

    # Ejecutar la consulta y leer los resultados en un DataFrame
    df = pd.read_sql(sql_query, conn)   # Cada registro del df es una lista de celdas
    df[col_cells] = df[col_cells].astype(str)   # Aseguramos que la columna de celdas sea un string
    df[col_cells] = df[col_cells].str.findall(r'\d+') # Con findall obtenemos una lista de strings
    print(df)

    # Cerrar la conexión con la base de datos
    conn.close()

    return df['variable'].to_numpy(), df[col_cells].to_numpy()

# recolectar_celdas('Personas', "('id_dep, 152.0')", 'UNAM_1057')
# recolectar_celdas('epi_puma_worldclim', "('Mean Diurnal Range (Mean of monthly (max temp - min temp)), 6.275:10.608')", 'mun')