# En plataforma se inidica un nombre para la misma

# lab_var es la columna donde están los nombres de la variables
# resolution indica la columna donde están las celdas para cada resolución del ensamble.
# interval es la columna donde están los intervalos
# table es la tabla donde están almacenados los datos

plataforma = {'name' : 'Personas y ecologia'}

fuente_de_datos_metadatos = {
        'Personas' : {
            'host' : 'fastdb.c3.unam.mx',
            'user' : 'monitor',
            'password' : 'monitor123',
            'port' : '5433',
            'lab_var' : 'nombre',
            'interval' : 'valor',
            'table' : 'covariable',
            'resolution' : {'UNAM_1057' : 'presencias'}
        },
        'epi_puma_worldclim' : {
            'host' : 'fastdb.c3.unam.mx',
            'user' : 'monitor',
            'password' : 'monitor123',
            'port' : '5433',
            'lab_var' : 'label',
            'interval' : 'interval',
            'table' : 'covariable',
            'resolution' :{'mun' : 'cells_mun',
                            'state' : 'cells_state'
                            }
        },
        'DB_Deforestacion' : {
            'host' : 'fastdb.c3.unam.mx',
            'user' : 'monitor',
            'password' : 'monitor123',
            'port' : '5433',
            'lab_var' : 'label',
            'interval' : 'tag',
            'table' : 'deforestacion',
            'resolution' :{'mun' : 'cells_mun'
                            }
        }
}

query_categorias = {
    'Personas' : '''
        select {lab_var} as nombre_variable,
        {interval} as intervalo,
        '"Personas"' as metadatos
        from {table}
        ;
    '''.format(lab_var = fuente_de_datos_metadatos['Personas']['lab_var'],
            interval = fuente_de_datos_metadatos['Personas']['interval'],
            table = fuente_de_datos_metadatos['Personas']['table']),
   
    'epi_puma_worldclim' : '''
        select {lab_var} as nombre_variable,
        {interval} as intervalo,
        '"epi_puma_worldclim"' as metadatos
        from {table}
        ;
    '''.format(lab_var = fuente_de_datos_metadatos['epi_puma_worldclim']['lab_var'],
                interval = fuente_de_datos_metadatos['epi_puma_worldclim']['interval'],
                table = fuente_de_datos_metadatos['epi_puma_worldclim']['table']),
    'DB_Deforestacion' : '''
        select {lab_var} as nombre_variable,
        {interval} as intervalo,
        '"Deforestacion"' as metadatos
        from {table}
        ;
    '''.format(lab_var = fuente_de_datos_metadatos['DB_Deforestacion']['lab_var'],
            interval = fuente_de_datos_metadatos['DB_Deforestacion']['interval'],
            table = fuente_de_datos_metadatos['DB_Deforestacion']['table']),
}