import yaml
with open('configuraciones_db/config_niche.yaml') as stream:
    config_loaded = yaml.safe_load(stream)
    plataforma = config_loaded['plataforma']
    fuente_de_datos_metadatos = config_loaded['fuente_de_datos_metadatos']

query_categorias = {
    'niche_integration' : '''
        select concat({lab_var}) as taxonomia_variable,

        concat(reinovalido,', ', phylumdivisionvalido,', ', clasevalida,', ', ordenvalido,', ', familiavalida,', ', generovalido) as metadatos
        from {table}
        ;
    '''.format(lab_var = fuente_de_datos_metadatos['niche_integration']['variable_columns'][0],
            table = fuente_de_datos_metadatos['niche_integration']['table'])
}