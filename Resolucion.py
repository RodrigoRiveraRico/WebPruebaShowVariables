from config import fuente_de_datos_metadatos

bases = ['epi_puma_censo_inegi_2020', 'epi_puma_worldclim', 'epi_puma_accidentes']

dic = {}    # Diccionario a construir. Resolucion : [base de datos]

for db in bases:    # Para cada base de las seleccionadas
    res_dict = fuente_de_datos_metadatos[db]['resolution']  # Se asigna el diccionario de resolucion de cada base
    for key in res_dict.keys(): # Cada key es una resolución
        if key not in dic:  # Si la resolucion no está en el diccionario
            dic.update({key:[]})    # Agregamos la resolución faltante cuyos valores será una lista de bases de datos
        dic[key].append(db) # Añadimos la base de datos a la resolución

print(dic)