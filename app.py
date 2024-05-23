from flask import Flask, render_template, request, jsonify
from PyPostQL import pruebasPostgres
from Var_Clss_Construction import dict_construction, df_construction
from tree_variables_from_db import creacion_ramas_arbol
from config import fuente_de_datos_metadatos

app = Flask(__name__)

data_bases = []
for db_name in fuente_de_datos_metadatos:
    data_bases.append(db_name)
print("Bases de datos disponibles: {}".format(data_bases))

selected_names = []



@app.route('/')
def index():
    return render_template('index.html', selected_names=selected_names, suggestions=data_bases)

@app.route('/add_name', methods=['POST'])
def add_name():
    name = request.form.get('name')
    if name and name not in selected_names:
        selected_names.append(name)
    return jsonify(selected_names=selected_names)

@app.route('/tree_data')
def get_tree_data():
    tree_data = [{"id": DB,
                 "text": DB, 
                 "children": creacion_ramas_arbol(DB)} for DB in selected_names]
    return jsonify(tree_data)

@app.route('/process', methods=['POST'])
def process():
    return render_template('arbol.html')#, data=selected_names, D_c=D_c)

@app.route('/select_variables', methods=['POST'])
def select_variables():
    selected_values1 = request.form['selectedVariables1']   # Covariables
    selected_values2 = request.form['selectedVariables2']   # Clase

    list_db_var = selected_values1.split('\r\n')
    list_db_clss = selected_values2.split('\r\n')

#### Construcción árbol (dict) de variables ####

    dict_db_variables = dict_construction(list_db_var)
#### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ####

#### Construcción árbol (dict) de clase ####

    dict_db_class = dict_construction(list_db_clss)
#### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ####

#### Construcción DataFrame de variables y clase ####
    df_all_variables_data = df_construction(dict_db_variables, 'Covariables')
    df_all_class_data = df_construction(dict_db_class, 'clase')

    df_all_variables_data['N_v'] = list(map(lambda x: len(set(x)), df_all_variables_data.iloc[:, -1]))
    df_all_variables_data['N_vnc'] = [conteo_interseccion(x, list(df_all_class_data.celdas)[0]) for x in list(df_all_variables_data.celdas)]

    nombre_clase = df_all_class_data.iloc[0, 0]

    df_final = df_all_variables_data.drop(['celdas'], axis=1)


    return render_template('resDf.html', df_resultado=df_final.to_html(), nombre_titulo=nombre_clase)

def conteo_interseccion(l_var, l_cov):
    return sum(1 for var in l_var if var in l_cov)

if __name__ == '__main__':
    app.run(debug=True)