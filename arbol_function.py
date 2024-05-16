### Definición de la función

def arbol(df):
  """
  df : pd.dataframe
       Columnas: | nombre_variable | metadatos | plataforma |
       Ordernar las variables de forma ascendente al número de niveles en el que están ubicadas.

  Return : dict
  """
  thisdict = {} # Diccionario a crear
  the_dict = '' # Va creando el diccionario llave por llave

  for idx in df.T:  # Iteración sobre índices del DataFrame

    the_dict = 'thisdict'

    for level_idx in range(len([df.loc[idx]['metadatos']])):  # Iteración sobre los índices de los metadatos

      level = df.loc[idx]['metadatos'] # Nivel de la categoría
  
      if level not in eval(the_dict):
        if level_idx < len([df.loc[idx]['metadatos']]) - 1:
          eval(the_dict).update({level: {}})
        else:
          eval(the_dict).update({level: {'__variables__' : []}}) # Aquí irán las variables en una lista

      the_dict += str([level])

      if '__variables__' in eval(the_dict) and df.loc[idx]['nombre_variable'] not in eval(the_dict)['__variables__'] and level_idx == len([df.loc[idx]['metadatos']]) - 1:
        eval(the_dict)['__variables__'].append(df.loc[idx]['nombre_variable'])

  return thisdict


def arbol2(df):
  thisdict = {} # Diccionario a crear
  the_dict = '' # Va creando el diccionario llave por llave

  for idx in df.T:  # Iteración sobre índices del DataFrame

    the_dict = 'thisdict'

    for level_idx in range(len([df.loc[idx]['metadatos']])):  # Iteración sobre los índices de los metadatos

      level_list = df.loc[idx]['metadatos'].split(', ') # Nivel de la categoría
      for level in level_list:

        if level not in eval(the_dict):
          if level_idx < len([df.loc[idx]['metadatos']]) - 1:
            eval(the_dict).update({level: {}})
          else:
            eval(the_dict).update({level: {'__variables__' : []}}) # Aquí irán las variables en una lista

        the_dict += str([level])

      if '__variables__' in eval(the_dict) and df.loc[idx]['nombre_variable'] not in eval(the_dict)['__variables__'] and level_idx == len([df.loc[idx]['metadatos']]) - 1:
        eval(the_dict)['__variables__'].append(df.loc[idx]['nombre_variable'])

  return thisdict