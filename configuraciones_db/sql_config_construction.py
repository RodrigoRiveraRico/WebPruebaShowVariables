def concatenacion_taxonomia(dict_db_values:dict):
    text_concat = ''
    for column in dict_db_values['variable_columns']:
        text_concat += column + ', '
    return text_concat[:-2]

def concatenacion_metadatos(dict_db_values:dict):
    text_concat = ''
    for column in dict_db_values['categorias']['columnas']:
        text_concat += column + ",', ', "
    return text_concat[:-7]

def table(dict_db_values:dict):
    return dict_db_values['table']