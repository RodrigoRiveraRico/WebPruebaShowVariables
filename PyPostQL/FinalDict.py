D_l = ['epi_puma_censo_inegi_2020: Población masculina', 
     'epi_puma_censo_inegi_2020: Población femenina de 6 a 11 años', 
     'epi_puma_worldclim: Annual Mean Temperature', 
     'epi_puma_worldclim: Precipitation of Wettest Month']


def lista_a_diccionario(lista):
    diccionario = {}
    
    for elemento in lista:
        clave, valor = elemento.split(':')
        clave = clave.strip()
        valor = valor.strip()
        if clave in diccionario:
            diccionario[clave].append(valor)
        else:
            diccionario[clave] = [valor]
    
    return diccionario

# # Ejemplo de uso
# lista = ['epi_1 : Pob 20', 'epi_2: Población 30', 'epi_1: Pob 40', 'epi_2: Pob 50']
# resultado = lista_a_diccionario(lista)
# print(resultado)

print(lista_a_diccionario(D_l))