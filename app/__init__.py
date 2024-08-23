from flask import Flask
import os

def create_app(plataforma, fuente_de_datos_metadatos, query_categorias, conexion):
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key###')
    # print(app.secret_key)

    # Cargar configuraciones
    app.config['PLATAFORMA'] = plataforma
    app.config['FUENTE_DE_DATOS_METADATOS'] = fuente_de_datos_metadatos
    app.config['QUERY_CATEGORIAS'] = query_categorias
    app.config['CONEXION'] = conexion
    
    # Importar y registrar rutas
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app
