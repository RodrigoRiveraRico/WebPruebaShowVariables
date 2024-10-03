from flask import Flask
import os

def create_app(plataforma, fuente_de_datos_metadatos):
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    # print(app.secret_key)

    # Cargar configuraciones
    app.config['PLATAFORMA'] = plataforma
    app.config['FUENTE_DE_DATOS_METADATOS'] = fuente_de_datos_metadatos
    
    # Importar y registrar rutas
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app
