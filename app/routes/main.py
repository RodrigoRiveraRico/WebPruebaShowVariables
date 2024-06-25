from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for, g
from app.Var_Clss_Construction import dict_construction, df_construction
from app.tree_variables_from_db import creacion_ramas_arbol
from app.Resolucion import ditc_res_DBs_list
import app.conteos as conteos
import pandas as pd
import os

main_bp = Blueprint('main', __name__)

@main_bp.before_app_request
def setup():
    # global data_bases, nombre_plataforma, fuente_de_datos_metadatos, plataforma
    session['fuente_de_datos_metadatos'] = current_app.config['FUENTE_DE_DATOS_METADATOS']
    session['plataforma'] = current_app.config['PLATAFORMA']
    session['data_bases'] = [db_name for db_name in session['fuente_de_datos_metadatos']]
    # print("Bases de datos disponibles: {}".format(data_bases))
    session['nombre_plataforma'] = session['plataforma']['name']

@main_bp.route('/')
def index():
    # global selected_names
    session['selected_names'] = []
    return render_template('index.html', selected_names=session['selected_names'], suggestions=session['data_bases'], etiqueta_h=session['nombre_plataforma'])

@main_bp.route('/add_name', methods=['POST'])
def add_name():
    name = request.form.get('name')
    if name not in session['selected_names']:
        session['selected_names'].append(name)
    return jsonify(selected_names=session['selected_names'])

@main_bp.route('/res_db', methods=['POST'])
def res_db():
    Dict_res = ditc_res_DBs_list(session['selected_names'])
    return render_template('resDB.html', Dict_res=Dict_res, etiqueta_h=session['nombre_plataforma'])

@main_bp.route('/process', methods=['POST'])
def process():
    # global selected_names_res, res
    selected_dbS = request.form['selected_res_DB']
    list_res_db = selected_dbS.split('\r\n')
    session['selected_names_res'] = [i.split(':')[1] for i in list_res_db]
    session['res'] = list_res_db[0].split(':')[0]
    return render_template('arbol.html', etiqueta_h=session['nombre_plataforma'])

@main_bp.route('/tree_data')
def get_tree_data():
    tree_data = [{"id": DB, "text": DB, "children": creacion_ramas_arbol(DB)} for DB in session['selected_names_res'] ]
    return jsonify(tree_data)

@main_bp.route('/select_variables', methods=['POST'])
def select_variables():

    # global nombre_clase, df_copia
    global df_copia

    selected_values1 = request.form['selectedVariables1']
    selected_values2 = request.form['selectedVariables2']

    list_db_var = selected_values1.split('\r\n')
    list_db_clss = selected_values2.split('\r\n')

    dict_db_variables = dict_construction(list_db_var)
    dict_db_class = dict_construction(list_db_clss)

    df_all_variables_data = df_construction(dict_db_variables, 'Covariable', session['res'])
    df_all_class_data = df_construction(dict_db_class, 'clase', session['res'])

    session['nombre_clase'] = df_all_class_data.iloc[0, 0]

    df_all_variables_data_notnull = df_all_variables_data[df_all_variables_data['celdas'].notnull()]
    df_all_variables_data = df_all_variables_data_notnull

    df_all_class_data_notnull = df_all_class_data[df_all_class_data['celdas'].notnull()]
    df_all_class_data = df_all_class_data_notnull

    csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'catalogos', 'catalogo_resoluciones.csv')
    df_resolutions = pd.read_csv(csv_path).set_index('resolution')
    N = df_resolutions.loc[session['res']]['N']

    conteos.df_count_cells(df_all_variables_data, df_all_class_data)
    conteos.epsilon(df_all_variables_data, N)
    conteos.score(df_all_variables_data)
    # session['df_copia'] = df_all_variables_data.to_dict(orient='records')
    df_copia = df_all_variables_data.to_dict(orient='records')
    return redirect(url_for('main.score_eps'))
    # return jsonify(df_all_variables_data.to_dict(orient='records'))

    df_all_cells_data = df_all_variables_data.explode('celdas').drop(columns=['epsilon'])
    df_all_cells_data = df_all_cells_data.rename(columns={'celdas': 'celda'})

    aggregations = {
        'Covariable': '<br>'.join,
        'score': 'sum'
    }
    df_all_cells_data = df_all_cells_data.groupby('celda').agg(aggregations).reset_index()
    df_all_cells_data = df_all_cells_data.rename(columns={'Covariable': 'Covariables'})

    df_all_variables_data.sort_values(by=['Covariable'], inplace=True)
    df_all_cells_data.sort_values(by=['Covariables'], inplace=True)

    return render_template('ScEp.html', 
                           df_resultado=df_all_variables_data.drop(['celdas'], axis=1).to_html(), 
                           df_resultado2=df_all_cells_data.to_html(escape=False),
                           nombre_titulo=nombre_clase,
                           etiqueta_h=nombre_plataforma)

#-- Rutas para poder filtrar los epsilons más significativos:
@main_bp.route('/score_eps', methods=['GET', 'POST'])
def score_eps():
    df_all_variables_data = pd.DataFrame.from_dict(df_copia)
    filter_value = request.args.get('filter', None)

    if filter_value == 'E_signif':
        df_all_variables_data = df_all_variables_data[df_all_variables_data['epsilon'].abs() > 2]

    df_all_cells_data = df_all_variables_data.explode('celdas').drop(columns=['epsilon'])
    df_all_cells_data = df_all_cells_data.rename(columns={'celdas': 'celda'})

    aggregations = {
        'Covariable': '<br>'.join,
        'score': 'sum'
    }
    df_all_cells_data = df_all_cells_data.groupby('celda').agg(aggregations).reset_index()
    df_all_cells_data = df_all_cells_data.rename(columns={'Covariable': 'Covariables'})

    df_all_variables_data.sort_values(by=['Covariable'], inplace=True)
    df_all_cells_data.sort_values(by=['Covariables'], inplace=True)


    return render_template('ScEp.html', df_resultado=df_all_variables_data.drop(['celdas'], axis=1).to_html(), 
                           df_resultado2=df_all_cells_data.to_html(escape=False), nombre_titulo=session['nombre_clase'],
                           etiqueta_h=session['nombre_plataforma'])