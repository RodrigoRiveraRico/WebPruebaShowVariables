import yaml
with open('configuraciones_db/config_niche.yaml') as stream:
    config_loaded = yaml.safe_load(stream)
    plataforma = config_loaded['plataforma']
    fuente_de_datos_metadatos = config_loaded['fuente_de_datos_metadatos']

def concatenacion_taxonomia(db_name:str):
    text_concat = ''
    for column in fuente_de_datos_metadatos[db_name]['variable_columns']:
        text_concat += column + ', '
    return text_concat[:-2]

def concatenacion_metadatos(db_name:str):
    text_concat = ''
    for column in fuente_de_datos_metadatos[db_name]['categorias']['columnas']:
        text_concat += column + ",', ', "
    return text_concat[:-7]

def table(db_name:str):
    return fuente_de_datos_metadatos[db_name]['table']

query_categorias = {}
for db_name in fuente_de_datos_metadatos:
    txt = f"""
        SELECT 
            CONCAT({concatenacion_taxonomia(db_name)}) as taxonomia_variable,
        
            CONCAT({concatenacion_metadatos(db_name)}) as metadatos

            FROM {table(db_name)}
        ;
        """
    query_categorias = {db_name : txt}

print(query_categorias)


query_categorias = {
    'niche_integration' : '''
        select concat({lab_var}) as taxonomia_variable,

        concat(reinovalido,', ', phylumdivisionvalido,', ', clasevalida,', ', ordenvalido,', ', familiavalida,', ', generovalido) as metadatos
        from {table}
        ;
    '''.format(lab_var = fuente_de_datos_metadatos['niche_integration']['variable_columns'][0],
            table = fuente_de_datos_metadatos['niche_integration']['table'])
}
print(query_categorias)