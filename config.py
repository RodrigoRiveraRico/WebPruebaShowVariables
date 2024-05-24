
# lab_var es la columna donde están los nombres de la variables
# cells es la columna donde están las celdas.
# interval es la columna donde están los intervalos

fuente_de_datos_metadatos = {
    'epi_puma_censo_inegi_2020' : {
        'host' : 'fastdb.c3.unam.mx',
        'user' : 'monitor',
        'password' : 'monitor123',
        'port' : '5433',
        'lab_var' : 'name',
        'cells' : 'cells_mun',
        'interval' : 'interval',
        'resolution' : {'mun' : 'cells_mun',
                        'state' : 'cells_state'
                        }
    },
    'epi_puma_worldclim' : {
        'host' : 'fastdb.c3.unam.mx',
        'user' : 'monitor',
        'password' : 'monitor123',
        'port' : '5433',
        'lab_var' : 'label',
        'cells' : 'cells_mun',
        'interval' : 'interval',
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
        'cells' : 'cells_mun',
        'interval' : 'interval',
        'resolution' : {'mun' : 'cells_mun'}
    },
     'newspecies' : {
        'host' : 'fastdb.c3.unam.mx',
        'user' : 'monitor',
        'password' : 'monitor123',
        'port' : '5433',
        'lab_var' : 'especievalida',
        'cells' : 'cells_mun',
        'interval' : 'nspn',
        'resolution' :{'mun' : 'cells_mun',
                       'state' : 'cells_state'
                       }
    }
}

query_categorias = {
    'epi_puma_censo_inegi_2020' : '''
        select case
        when name like 'Grado promedio%' then name
        when name like '%afiliada%servicios%' then name
        when name like '%condici_n mental%' or name like '%discapacidad%' or name like '%limitaci_n%' then name
        when name like '%censales%referencia%' or name like '%viviendas particulares%' or name like '%religi_n%' or name like '%a_os%' or name like '%poblaci_n nacida%entidad%' then name
        when name like '%poblaci_n femeninca%' or name like '%pobalci_n masculina' then name
        when name like '%viviendas particulares%' then name
        when name like '%viviendas particulares habitadas que no%' then name
        else name 
    end as nombre_variable,

    interval as intervalo,

    case 
        when name like 'Grado promedio%' then concat('estudios',', ','escolaridad') 
        when name like '%afiliada%servicios%' then concat('salud',', ','servicios salud')
        when name like '%condici_n mental%' or name like '%discapacidad%' or name like '%limitaci_n%' then concat('salud',', ','discapacidad')
        when name like '%censales%referencia%' or name like '%viviendas particulares%' or name like '%religi_n%' or name like '%a_os%' or name like '%poblaci_n nacida%entidad%' then concat('personas',', ','población')
        when name like '%poblaci_n femeninca%' or name like '%pobalci_n masculina' then concat('personas',', ','genero')
        when name like '%viviendas particulares%' then concat('vivienda',', ','vivienda1')
        when name like '%viviendas particulares habitadas que no%' then concat('vivienda',', ','vivienda2')
        else concat('Otros')
    end as metadatos

    from covariable
    ;
    ''' ,

    'epi_puma_worldclim' : '''
        select label as nombre_variable,
        interval as intervalo,
        '"epi_puma_worldclim"' as metadatos
        from covariable
        ;
    ''',

    'epi_puma_accidentes' : '''
        select name as nombre_variable,
        interval as intervalo,
        '"epi_puma_accidentes"' as metadatos
        from covariable
        ;
        ''',

    'newspecies' : '''
        select especievalida as nombre_variable,
        nspn as intervalo,
        concat(reinovalido,', ', phylumdivisionvalido,', ', clasevalida,', ', ordenvalido,', ', familiavalida,', ', generovalido) as metadatos
        from covariable
        ;
        '''
}
