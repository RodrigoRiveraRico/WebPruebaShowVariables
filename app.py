from flask import Flask, render_template, request, jsonify
from Var_Clss_Construction import dict_construction, df_construction
from tree_variables_from_db import creacion_ramas_arbol
from Resolucion import ditc_res_DBs_list
import conteos
import pandas as pd
from config import fuente_de_datos_metadatos, plataforma

app = Flask(__name__)

data_bases = []
for db_name in fuente_de_datos_metadatos:
    data_bases.append(db_name)
print("Bases de datos disponibles: {}".format(data_bases))

nombre_plataforma = plataforma['name']

# 1.- =============== Página principal (Seleccionar DBs) ----------
@app.route('/')
def index():
    global selected_names
    selected_names = []
    return render_template('index.html', selected_names=selected_names, suggestions=data_bases, etiqueta_h=nombre_plataforma)

@app.route('/add_name', methods=['POST'])
def add_name():
    name = request.form.get('name')
    if name and name not in selected_names:
        selected_names.append(name)
    return jsonify(selected_names=selected_names)


# 2.- =============== Seleccionar resoluciones compatibles de las DBs -------
@app.route('/res_db', methods=['POST'])
def res_db():
    Dict_res = ditc_res_DBs_list(selected_names)
    return render_template('resDB.html', Dict_res = Dict_res, etiqueta_h=nombre_plataforma)



# 3.- =============== Seleccionar los conjuntos de covariables y la clase (Árbol) -------
# selected_names_res = []     # Nuevo selected names actualizado, con otro nombre.
res = ''   # nombre de la resolución escogida

@app.route('/process', methods=['POST'])
def process():
    global selected_names_res   # Para que se actualice también en /tree_data
    selected_dbS = request.form['selected_res_DB']   # Llamamos el textarea.
    list_res_db = selected_dbS.split('\r\n')  # es de la forma [res:db1, res:bd2]
    selected_names_res = [i.split(':')[1] for i in list_res_db]      #Selected names actualizado
    global res
    res = list_res_db[0].split(':')[0]  #actualización de res.
    return render_template('arbol.html',  etiqueta_h=nombre_plataforma)

@app.route('/tree_data')   # Formar el arbol que se muestra
def get_tree_data():
    tree_data = [{"id": DB,
                 "text": DB, 
                 "children": creacion_ramas_arbol(DB)} for DB in selected_names_res]
    return jsonify(tree_data)


# 4.- =============== Desplegar las tablas con los cáclulos de Score y epsilon (pág. final) -------
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

    df_all_variables_data = df_construction(dict_db_variables, 'Covariable', res)
    df_all_class_data = df_construction(dict_db_class, 'clase', res)

    # Extraemos el nombre de la clase
    nombre_clase = df_all_class_data.iloc[0, 0]
#### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ####

#### Nos interesan los datos que tengan registros distintos a None o NaN ####
    # Nota: Hay que excluir los registros que tienen None.
    # Valdría la pena indicar cuáles registros tienen None.
    df_all_variables_data_notnull = df_all_variables_data[df_all_variables_data['celdas'].notnull()]
    df_all_variables_data = df_all_variables_data_notnull

    df_all_class_data_notnull = df_all_class_data[df_all_class_data['celdas'].notnull()]
    df_all_class_data = df_all_class_data_notnull
#### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ####
    # print(df_all_variables_data.dtypes)

#### Contamos el número de celdas de variables y clase ####
    # Leemos el catálogo de resoluciones
    df_resolutions = pd.read_csv('Catalogos/catalogo_resoluciones.csv').set_index('resolution')
    # Obtenemos la N del ensamble
    N = df_resolutions.loc[res]['N']

    # Las siguientes líneas modifican la tabla original df_all_variables_data
    conteos.df_count_cells(df_all_variables_data, df_all_class_data)
    conteos.epsilon(df_all_variables_data, N)
    conteos.score(df_all_variables_data)

    # Creamos un nuevo DataFrame con las celdas desanidadas.
    # Este DataFrame ya no emplea la columna 'score'.
    df_all_cells_data = df_all_variables_data.explode('celdas').drop(columns=['score'])

    # Cambiamos el nombre de la columna 'celdas' por 'celda' para indicar que cada registro corresponde a una única celda.
    df_all_cells_data = df_all_cells_data.rename(columns={'celdas':'celda'})

    # Definimos las funciones de agregación para cada columna
    # Utilizamos '<br>' para generar el salto de línea en HTML
    aggregations = {
        'Covariable': '<br>'.join,
        'epsilon': 'sum'
        }
    # Aplicamos groupby con agg
    df_all_cells_data = df_all_cells_data.groupby('celda').agg(aggregations).reset_index()

    # Renombramos la columna 'Covariable' por 'Covariables' para indicar que cada registro corresponde a una o varias covariables.
    df_all_cells_data = df_all_cells_data.rename(columns={'Covariable':'Covariables'})

    return render_template('resDF.html', 
                           df_resultado = df_all_variables_data.drop(['celdas'],axis=1).to_html(), 
                           df_resultado2 = df_all_cells_data.to_html(escape=False),
                           nombre_titulo = nombre_clase,
                           etiqueta_h=nombre_plataforma)

if __name__ == '__main__':
    app.run(debug=True)