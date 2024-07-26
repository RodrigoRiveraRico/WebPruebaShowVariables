import yaml
import configuraciones_db.sql_config_construction as sql_c
with open('configuraciones_db/config_default.yaml') as stream:
    config_loaded = yaml.safe_load(stream)
    plataforma = config_loaded['plataforma']
    fuente_de_datos_metadatos = config_loaded['fuente_de_datos_metadatos']

query_categorias = {}
for db_name, db_config_values in fuente_de_datos_metadatos.items():
    if db_config_values['categorias'] == None:
        metadatos_txt = f'{db_name}'

    elif isinstance(db_config_values['categorias'], dict):
        metadatos_txt = f'CONCAT({sql_c.concatenacion_metadatos(db_config_values)})'
    
    elif isinstance(db_config_values['categorias'], str):
        exec("from configuraciones_db."+db_config_values['categorias'][:-3]+" import txt")
        metadatos_txt = eval('txt')
    
    txt = f"""
        SELECT 
            CONCAT({sql_c.concatenacion_taxonomia(db_config_values)}) as taxonomia_variable,

            {metadatos_txt} as metadatos

        FROM {sql_c.table(db_config_values)}
        ;
        """
    query_categorias.update({db_name : txt})