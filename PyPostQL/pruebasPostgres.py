import psycopg2
import pandas as pd
from config import fuente_de_datos_metadatos


def recolectar_variables(DB:str):
    conn = psycopg2.connect(database = DB, 
                            user = fuente_de_datos_metadatos[DB]['user'], 
                            host= fuente_de_datos_metadatos[DB]['host'],
                            password = fuente_de_datos_metadatos[DB]['password'],
                            port = fuente_de_datos_metadatos[DB]['port']
                            )

    col = fuente_de_datos_metadatos[DB]['col']
    lab_var = fuente_de_datos_metadatos[DB]['lab_var']
    interval = fuente_de_datos_metadatos[DB]['interval']
    
    # Definir la consulta SQL para leer los primeros 20 renglones de la tabla
    # sql_query = "SELECT "+lab_var+" FROM public.covariable WHERE " + col + " = 1 LIMIT 10;"
    sql_query = "SELECT " + "concat("+lab_var+",', ',"+interval+")" + " FROM public.covariable ORDER BY " + lab_var +", "+ col + " LIMIT 20;"

    # Ejecutar la consulta y leer los resultados en un DataFrame
    df = pd.read_sql(sql_query, conn)
    # Obtenemos la primer columna y la convertimos a lista
    variables = df.iloc[:,0].tolist()
    # Cerrar la conexión con la base de datos
    conn.close()
    return variables