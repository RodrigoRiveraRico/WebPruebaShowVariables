import requests
import pandas as pd

def tree_from_endpoint(DB: str, fuente_de_datos_metadatos: dict):
    '''
    Función que se emplea con la configuración para conectar endpoints.
    Esta función hace la conexión a un endpoint.

    Return: DataFrame
    '''
    api_url = fuente_de_datos_metadatos[DB]['variables']
    response = requests.get(api_url).json()
    df_response = pd.json_normalize(response)
    df_response.rename(columns={'name':'taxonomia_variable'}, inplace=True)
    df_response['metadatos'] = DB   # Aparecerá 2 veces el nombre de la base en el árbol
    df = df_response[['id', 'taxonomia_variable', 'metadatos']]

    return df

def cells_from_endpoint(DB: str, variables: list, res: str, fuente_de_datos_metadatos: dict):
    '''
    Función que se emplea con la configuración para conectar endpoints.
    Esta función hace la conexión a un endpoint.

    Return: Tupla de arreglos numpy
    '''
    data = []
    for idx in variables:
        api_url = fuente_de_datos_metadatos[DB]['get_data']
        api_url = api_url + '/' + str(idx) + '?grid_id=' + res
        response = requests.get(api_url).json()[0]
        data.append({'id': str(response['id']), 'cells': response['cells']})
    df_response = pd.json_normalize(data)
    df_response['cells'] = df_response['cells'].astype(str)
    df_response['cells'] = df_response['cells'].str.findall(r'\d+')
    # print(df_response)

    variables_url = fuente_de_datos_metadatos[DB]['variables']
    variables_response = requests.get(variables_url).json()
    df_variables_response = pd.json_normalize(variables_response)[['id', 'name']]
    df_variables_response['id'] = df_variables_response['id'].astype(str)
    df_variables_response['name'] = df_variables_response['name'].str.replace('_-_', ', ')

    df_joined = df_variables_response.join(df_response.set_index('id'), on='id', how='inner')
    # print(df_joined)

    return df_joined['name'].to_numpy(), df_joined['cells'].to_numpy()