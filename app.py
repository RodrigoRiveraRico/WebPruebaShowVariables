from flask import Flask, render_template, request, jsonify
from PyPostQL import pruebasPostgres, FinalDict, retrieve_cells
import pandas as pd
import numpy as np
import random
import json
import conteos
from Var_Clss_Construction import dict_construction, df_construction
from config import fuente_de_datos_metadatos

print(random.randint(0,9))

app = Flask(__name__)

data_bases = []
for db_name in fuente_de_datos_metadatos:
    data_bases.append(db_name)
print("Bases de datos disponibles: {}".format(data_bases))

# Diccionario predefinido
# D_c = {'epi_puma_censo_inegi_2020': [1,2,3], 'epi_puma_worldclim':[4,5,6], 'DB_3': [7,8,9]}

selected_names = []

@app.route('/')
def index():
    return render_template('index.html', selected_names=selected_names, suggestions = data_bases)

@app.route('/add_name', methods=['POST'])
def add_name():
    name = request.form.get('name')
    if name not in selected_names:
        selected_names.append(name)
    return jsonify(selected_names=selected_names)

# D_c = {}
# for i in selected_names:
#     D_c[i] = [1,random.randint(0,9),random.randint(0,9)]
# print(pruebasPostgres.prove1())
# print(selected_names)
# D_c = {'epi_puma_censo_inegi_2020': [1,2,3], 'epi_puma_worldclim':[4,5,6], 'DB_3': [7,8,9]}

@app.route('/process', methods=['POST'])
def process():
    D_c = {}
    for i in selected_names:
        # Obtenemos las variables de cada DB seleccionada y las agregamos a un diccionario.
        L_v = pruebasPostgres.recolectar_variables(i)   # i es la base de datos (DB)
        D_c[i] = L_v
    # print(selected_names)
    return render_template('results.html', selected_names=selected_names, D_c=D_c)


@app.route('/select_variables', methods=['POST'])
def select_variables():
    selected_values1 = request.form['selectedValues1']  # Variables
    selected_values2 = request.form['selectedValues2']  # Clase


    list_db_var = selected_values1.split('\r\n')
    list_db_clss = selected_values2.split('\r\n')

#### Construcción árbol (dict) de variables ####

    dict_db_variables = dict_construction(list_db_var)
#### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ####

#### Construcción árbol (dict) de clase ####

    dict_db_class = dict_construction(list_db_clss)
#### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ####

#### Construcción DataFrame de variables y clase ####
    df_all_variables_data = df_construction(dict_db_variables, 'variables')
    df_all_class_data = df_construction(dict_db_class, 'clase')

    print(df_all_variables_data)
    print(df_all_class_data)

    conteos.df_count_cells(df_all_variables_data, df_all_class_data)    # Esta línea modifica la tabla original df_all_variables_data

    # Guardar en un archivo .csv
    # df_all_variables_data.to_csv('TablaFinal.csv', index=False)

    nombre_clase = df_all_class_data.iloc[0, 0]
    
    # return render_template('resDf.html', df_resultado=df_all_variables_data.to_html(),nombre_titulo=nombre_clase)
    return str(dict_db_variables) + '~'*10 + str(dict_db_class)


if __name__ == '__main__':
    app.run(debug=True)