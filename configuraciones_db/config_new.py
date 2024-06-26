# En plataforma se inidica un nombre para la misma

# lab_var es la columna donde están los nombres de la variables
# resolution indica la columna donde están las celdas para cada resolución del ensamble.
# interval es la columna donde están los intervalos
# table es la tabla donde están almacenados los datos

plataforma = {'name' : 'INEGI y especies'}

fuente_de_datos_metadatos = {
    'epi_puma_censo_inegi_2020' : {
        'host' : 'fastdb.c3.unam.mx',
        'user' : 'monitor',
        'password' : 'monitor123',
        'port' : '5433',
        'lab_var' : ['name', 'interval'],   # Cambiar nombre de 'lab_var'
        'table' : 'covariable',
        'resolution' : {'mun' : 'cells_mun',
                        'state' : 'cells_state',
                        'ageb' : 'cells_ageb'
                        }
    },
    'newspecies' : {
        'host' : 'fastdb.c3.unam.mx',
        'user' : 'monitor',
        'password' : 'monitor123',
        'port' : '5433',
        'lab_var' : ['especievalida'],
        'table' : 'covariable',
        'resolution' :{'mun' : 'cells_mun',
                        'state' : 'cells_state'}
    }     
}

query_categorias = {
    'epi_puma_censo_inegi_2020' : '''
        select concat({lab_var},'_-_',{interval}) as taxonomia_variable,

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
    '''.format(lab_var = fuente_de_datos_metadatos['epi_puma_censo_inegi_2020']['lab_var'][0],
            interval = fuente_de_datos_metadatos['epi_puma_censo_inegi_2020']['lab_var'][1],
            table = fuente_de_datos_metadatos['epi_puma_censo_inegi_2020']['table']),

    'newspecies' : '''
        select {lab_var} as taxonomia_variable,
        concat(reinovalido,', ', phylumdivisionvalido,', ', clasevalida,', ', ordenvalido,', ', familiavalida,', ', generovalido) as metadatos
        from {table}
        ;
    '''.format(lab_var = fuente_de_datos_metadatos['newspecies']['lab_var'][0],
            table = fuente_de_datos_metadatos['newspecies']['table'])
            }