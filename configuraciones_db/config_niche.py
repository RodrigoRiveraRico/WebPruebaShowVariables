import yaml
from configuraciones_db.sql_config_construction import concatenacion_metadatos, concatenacion_taxonomia, table
with open('configuraciones_db/config_niche.yaml') as stream:
    config_loaded = yaml.safe_load(stream)
    plataforma = config_loaded['plataforma']
    fuente_de_datos_metadatos = config_loaded['fuente_de_datos_metadatos']

query_categorias = {}
for db_name, db_values in fuente_de_datos_metadatos.items():
    txt = f"""
        SELECT 
            CONCAT({concatenacion_taxonomia(db_values)}) as taxonomia_variable,
        
            CONCAT({concatenacion_metadatos(db_values)}) as metadatos

            FROM {table(db_values)}
        ;
        """
    query_categorias = {db_name : txt}