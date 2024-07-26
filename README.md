Ejecución: 
- WINDOWS:
  
$ set FLASK_CONFIG_FILE=config_default
$ set SECRET_KEY=secret_key_de_tu_entorno_de_ejecucion

$ flask --app run run --port=4000 --host=0.0.0.0

- LINUX:

$ export FLASK_CONFIG_FILE=config_default
$ export SECRET_KEY='secret_key_de_tu_entorno_de_ejecucion'

$ flask --app run run --port=4000 --host=0.0.0.0

Ejemplo del archivo config.py
    
    
    # En plataforma se inidica un nombre para la misma
    
    # lab_var es la columna donde están los nombres de la variables
    # resolution indica la columna donde están las celdas para cada resolución del ensamble.
    # interval es la columna donde están los intervalos
    # table es la tabla donde están almacenados los datos
    
    plataforma = {'name' : 'Plataforma 1'}
    
    fuente_de_datos_metadatos = {
        'epi_puma_censo_inegi_2020' : {
            'host' : 'fastdb.c3.unam.mx',
            'user' : 'monitor',
            'password' : 'monitor123',
            'port' : '5433',
            'lab_var' : 'name',
            'interval' : 'interval',
            'table' : 'covariable',
            'resolution' : {'mun' : 'cells_mun',
                            'state' : 'cells_state',
                            'ageb' : 'cells_ageb'
                            }
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
         'epi_puma_accidentes' : {
            'host' : 'fastdb.c3.unam.mx',
            'user' : 'monitor',
            'password' : 'monitor123',
            'port' : '5433',
            'lab_var' : 'name',
            'interval' : 'interval',
            'table' : 'covariable',
            'resolution' : {'mun' : 'cells_mun'}
        },
         'newspecies' : {
            'host' : 'fastdb.c3.unam.mx',
            'user' : 'monitor',
            'password' : 'monitor123',
            'port' : '5433',
            'lab_var' : 'especievalida',
            'interval' : 'nspn',
            'table' : 'covariable',
            'resolution' :{'mun' : 'cells_mun',
                           'state' : 'cells_state'
                           }
        },
         'epi_puma_hospederos' : {
             'host' : 'fastdb.c3.unam.mx',
             'user' : 'monitor',
             'password' : 'monitor123',
             'port' : '5433',
             'lab_var' : 'nombrecientifico',
             'interval' : 'id',
             'table' : 'covariable',
             'resolution' : {'mun' : 'cells_mun',
                             'state' : 'cells_state'}
         }
    }
    
    query_categorias = {
        'epi_puma_censo_inegi_2020' : '''
            select {lab_var} as nombre_variable,
            {interval} as intervalo,
    
            case 
                when {lab_var} like 'Grado promedio%' then concat('estudios',', ','escolaridad') 
                when {lab_var} like '%afiliada%servicios%' then concat('salud',', ','servicios salud')
                when {lab_var} like '%condici_n mental%' or {lab_var} like '%discapacidad%' or {lab_var} like '%limitaci_n%' then concat('salud',', ','discapacidad')
                when {lab_var} like '%censales%referencia%' or {lab_var} like '%viviendas particulares%' or {lab_var} like '%religi_n%' or {lab_var} like '%a_os%' or {lab_var} like '%poblaci_n nacida%entidad%' then concat('personas',', ','población')
                when {lab_var} like '%poblaci_n femeninca%' or {lab_var} like '%pobalci_n masculina' then concat('personas',', ','genero')
                when {lab_var} like '%viviendas particulares%' then concat('vivienda',', ','vivienda1')
                when {lab_var} like '%viviendas particulares habitadas que no%' then concat('vivienda',', ','vivienda2')
                else concat('Otros')
            end as metadatos
    
            from {table}
            ;
        '''.format(lab_var = fuente_de_datos_metadatos['epi_puma_censo_inegi_2020']['lab_var'],
                interval = fuente_de_datos_metadatos['epi_puma_censo_inegi_2020']['interval'],
                table = fuente_de_datos_metadatos['epi_puma_censo_inegi_2020']['table']),
    
        'epi_puma_worldclim' : '''
            select {lab_var} as nombre_variable,
            {interval} as intervalo,
            '"epi_puma_worldclim"' as metadatos
            from {table}
            ;
        '''.format(lab_var = fuente_de_datos_metadatos['epi_puma_worldclim']['lab_var'],
                   interval = fuente_de_datos_metadatos['epi_puma_worldclim']['interval'],
                   table = fuente_de_datos_metadatos['epi_puma_worldclim']['table']),
    
        'epi_puma_accidentes' : '''
            select {lab_var} as nombre_variable,
            {interval} as intervalo,
            '"epi_puma_accidentes"' as metadatos
            from {table}
            ;
        '''.format(lab_var = fuente_de_datos_metadatos['epi_puma_accidentes']['lab_var'],
                interval = fuente_de_datos_metadatos['epi_puma_accidentes']['interval'],
                table = fuente_de_datos_metadatos['epi_puma_accidentes']['table']),
    
        'newspecies' : '''
            select {lab_var} as nombre_variable,
            {interval} as intervalo,
            concat(reinovalido,', ', phylumdivisionvalido,', ', clasevalida,', ', ordenvalido,', ', familiavalida,', ', generovalido) as metadatos
            from {table}
            ;
        '''.format(lab_var = fuente_de_datos_metadatos['newspecies']['lab_var'],
                interval = fuente_de_datos_metadatos['newspecies']['interval'],
                table = fuente_de_datos_metadatos['newspecies']['table']),
    
        'epi_puma_hospederos' : '''
            select {lab_var} as nombre_variable,
            {interval} as intervalo,
            concat(reino,', ', phylum,', ', clase,', ', orden,', ', familia,', ', genero) as metadatos
            from {table}
            ;
        '''.format(lab_var = fuente_de_datos_metadatos['epi_puma_hospederos']['lab_var'],
                interval = fuente_de_datos_metadatos['epi_puma_hospederos']['interval'],
                table = fuente_de_datos_metadatos['epi_puma_hospederos']['table'])
    }
