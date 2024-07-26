col = 'name'

txt = f'''
CASE 
    WHEN {col} LIKE 'Grado promedio%' THEN CONCAT('estudios',', ','escolaridad') 
    WHEN {col} LIKE '%afiliada%servicios%' THEN CONCAT('salud',', ','servicios salud')
    WHEN {col} LIKE '%condici_n mental%' or {col} LIKE '%discapacidad%' or {col} LIKE '%limitaci_n%' THEN CONCAT('salud',', ','discapacidad')
    WHEN {col} LIKE '%censales%referencia%' or {col} LIKE '%viviendas particulares%' or {col} LIKE '%religi_n%' or {col} LIKE '%a_os%' or {col} LIKE '%poblaci_n nacida%entidad%' THEN CONCAT('personas',', ','población')
    WHEN {col} LIKE '%poblaci_n femeninca%' or {col} LIKE '%pobalci_n masculina' THEN CONCAT('personas',', ','genero')
    WHEN {col} LIKE '%viviendas particulares%' THEN CONCAT('vivienda',', ','vivienda1')
    WHEN {col} LIKE '%viviendas particulares habitadas que no%' THEN CONCAT('vivienda',', ','vivienda2')
    ELSE CONCAT('Otros')
END
'''
