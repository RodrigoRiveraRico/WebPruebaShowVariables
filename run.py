from psycopg2 import connect, OperationalError
import csv
import os
import sys

# Obtener el archivo de configuración desde la variable de entorno
config_file = os.getenv('FLASK_CONFIG_FILE', 'configuraciones_db/config_1.py')

# Verificar si el archivo de configuración existe
if not os.path.isfile(config_file):
    print(f"Error: El archivo de configuración '{config_file}' no existe.")
    sys.exit(1)

# Ejecutar el archivo de configuración
config_globals = {}
try:
    with open(config_file) as f:
        exec(f.read(), config_globals)
except Exception as e:
    print(f"Error al ejecutar el archivo de configuración '{config_file}': {e}")
    sys.exit(1)

# Verificar que las variables necesarias están definidas
required_vars = ['plataforma', 'fuente_de_datos_metadatos', 'query_categorias']
for var in required_vars:
    if var not in config_globals:
        print(f"Error: La variable '{var}' no está definida en el archivo de configuración.")
        sys.exit(1)

plataforma = config_globals['plataforma']
fuente_de_datos_metadatos = config_globals['fuente_de_datos_metadatos']
query_categorias = config_globals['query_categorias']

# Verificar conexión
try:
    flag = False
    for DB in fuente_de_datos_metadatos.keys():
        try: 
            conn = connect(database = DB,
                        user = fuente_de_datos_metadatos[DB]['user'],
                        host = fuente_de_datos_metadatos[DB]['host'],
                        password = fuente_de_datos_metadatos[DB]['password'],
                        port = fuente_de_datos_metadatos[DB]['port'])
        except OperationalError as e:
            print(f'Unable to connect! {DB}\n{e}')
            flag = True
        else: 
            print(f'Connected! {DB}' )
            conn.close()
finally:
    if flag == True:
        sys.exit(1)

# Verificar resolucciones en catálogo
csv_path_catalogo = os.path.join(os.path.dirname(__file__), 'catalogos', 'catalogo_resoluciones.csv')
try:
    with open(csv_path_catalogo, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        resoluciones_catalogo = [row[0] for row in csv_reader]
except Exception as e:
    print(f"Error al ejecutar el archivo de catálogos '{config_file}': {e}")
    sys.exit(1)

flag = False
for DB in fuente_de_datos_metadatos.keys():
    resoluciones = list(fuente_de_datos_metadatos[DB]['resolution'].keys())
    if resoluciones == []:
        print(f"No hay resoluciones definidas en la configuración de {DB}")
        flag = True
    for res in resoluciones:
        if res not in resoluciones_catalogo:
            print(f"Resolución '{res}' de {DB} mal definida en el archivo de configuración.")
            flag = True
if flag == True:
    sys.exit(1)

from app import create_app

# Crear la aplicación Flask
app = create_app(plataforma, fuente_de_datos_metadatos, query_categorias)

if __name__ == '__main__':
    app.run(debug=True)
