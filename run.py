import os
from prueba_error import try_connection

# Obtener el archivo de configuración desde la variable de entorno
config_file = os.getenv('FLASK_CONFIG_FILE', 'configuraciones_db/config_1.py')

# Ejecutar el archivo de configuración
config_globals = {}
with open(config_file) as f:
    exec(f.read(), config_globals)

plataforma = config_globals['plataforma']
fuente_de_datos_metadatos = config_globals['fuente_de_datos_metadatos']
query_categorias = config_globals['query_categorias']

from app import create_app

# Crear la aplicación Flask
app = create_app(plataforma, fuente_de_datos_metadatos, query_categorias)

if __name__ == '__main__':
    try_connection(fuente_de_datos_metadatos)
    app.run(debug=True)
