import os

def concatenacion_taxonomia(db_config_values: dict) -> str:
    return ",'_-_',".join(db_config_values['variable_columns'])

def concatenacion_metadatos(db_config_values: dict) -> str:
    return "', ', ".join(db_config_values['categorias']['columnas'])

def table(db_config_values: dict) -> str:
    return db_config_values['table']