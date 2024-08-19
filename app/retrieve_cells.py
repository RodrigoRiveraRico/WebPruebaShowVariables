import pandas as pd
from flask import current_app
from sqlalchemy import create_engine, text

def recolectar_celdas(DB:str, variables:list, res:str):
    '''
    Función que obtiene, para cada variable, la lista de celdas donde hay presencia de estas.
    '''
    def conexion_psql():
        '''
        Función que hace la conexión a postgresql.

        Return : DataFrame
        '''
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

        # Lista de columnas donde está almacenada la taxonomía de las variables.
        tax_var_cols = fuente_de_datos_metadatos[DB]['variable_columns']

        # String que une la taxonomía de las variables
        columnas_variable = ",', ',".join(tax_var_cols)

        # Nombre de la tabla
        table = fuente_de_datos_metadatos[DB]['table']

        # Consulta
        sql_query = text(f'''
            WITH data AS (
                SELECT CONCAT({columnas_variable}) AS variable,
                {col_cells}
                FROM {table}
                )
            SELECT variable, {col_cells} 
            FROM data 
            WHERE variable IN :variables;
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

    def conexion_endpoint():
        import requests
        data = []
        for idx in variables:
            api_url = f'http://127.0.0.1:5000/get-data/{idx}?grid_id=mun'
            response = requests.get(api_url).json()[0]
            data.append({'id':str(response['id']), 'cells':response['cells']})
        df_response = pd.json_normalize(data)
        df_response['cells'] = df_response['cells'].astype(str)
        df_response['cells'] = df_response['cells'].str.findall(r'\d+')
        # print(df_response)

        variables_url = 'http://127.0.0.1:5000/variables'
        variables_response = requests.get(variables_url).json()
        df_variables_response = pd.json_normalize(variables_response)[['id', 'name']]
        df_variables_response['id'] = df_variables_response['id'].astype(str)

        df_joined = df_variables_response.join(df_response.set_index('id'), on='id', how='inner')
        # print(df_joined)

        return df_joined['name'].to_numpy(), df_joined['cells'].to_numpy()
        # return df_response['id'].to_numpy(), df_response['cells'].to_numpy()

    # print(conexion_endpoint())
    return conexion_endpoint()

# Ejemplo de uso
# variables = ['Annual Mean Temperature, 13.525:15.225', 'Annual Mean Temperature, 15.225:16.146', ...]
# recolectar_celdas('Personas', variables, 'UNAM_1057')
# recolectar_celdas('epi_puma_worldclim', variables, 'mun')