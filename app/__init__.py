from flask import Flask

def create_app(plataforma, fuente_de_datos_metadatos, query_categorias):
    app = Flask(__name__)
    
    # Cargar configuraciones
    app.config['PLATAFORMA'] = plataforma
    app.config['FUENTE_DE_DATOS_METADATOS'] = fuente_de_datos_metadatos
    app.config['QUERY_CATEGORIAS'] = query_categorias
    
    # Importar y registrar rutas
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app
