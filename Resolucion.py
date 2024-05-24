from config import fuente_de_datos_metadatos

bases = ['epi_puma_censo_inegi_2020', 'epi_puma_worldclim', 'epi_puma_accidentes']

dic = {}

for db in bases:
    ls =[]
    res_dict = fuente_de_datos_metadatos[db]['resolution']
    ls.append(db)
    for key in res_dict.keys():
        if key not in dic:
            dic.update({key:[]})
        dic[key].append(db)

print(dic)

