from flask import current_app

def ditc_res_DBs_list(bases):
    '''
    bases : lst Lista de bases de datos


    Return : dict {'resolución1' : [DB1, DB2,], 'resolución2' : [DB1, DB3,],}
    '''
    dic = {}    # Diccionario a construir.
    fuente_de_datos_metadatos = current_app.config['FUENTE_DE_DATOS_METADATOS']
    
    def with_psql():

        for db in bases:    # Para cada base de las seleccionadas
            res_dict = fuente_de_datos_metadatos[db]['resolution']  # Se asigna el diccionario de resolucion de cada base
            for key in res_dict.keys(): # Cada key es una resolución
                if key not in dic:  # Si la resolucion no está en el diccionario
                    dic.update({key:[]})    # Agregamos la resolución faltante cuyos valores será una lista de bases de datos
                dic[key].append(db) # Añadimos la base de datos a la resolución
        return dic
    
    def with_endpoint():
        db = bases[0]
        dic = {'mun':[db]}  

        return dic

    dic = with_endpoint()
    # print(dic)
    return dic