### 14/05/2024


from flask import Flask, render_template, request, jsonify
from PyPostQL import pruebasPostgres
from Var_Clss_Construction import dict_construction, df_construction
from prueba import creacion_ramas_arbol

app = Flask(__name__)

data_bases = ["epi_puma_censo_inegi_2020", "epi_puma_worldclim", "epi_puma_accidentes"]
selected_names = []

# tree_data = creacion_ramas_arbol()
# tree_data = [
#     {
#         "id": "Node 1",
#         "text": "epi_puma_censo_inegi_2020",
#         'state': {'opened': True},
#         "attr": {"nivel": "root", "type": 0},
#         "children": [
#             {"id": "Node 2", "text": "Node 2", "children": [{"id": "Hijo2", "text": "Grado promedio de escolaridad, 0.00%:0.01%"}]},
#             {"id": "node3", "text": "Node 3", "children": [
#                 {"id": "Hijo5", "text": "Hijo 5", "children": [{"id": "Hijo5.1", "text": "Población masculina"}]},
#                 {"id": "Hijo6", "text": "Hijo 6", "children": [
#                     {"id": "Hijo6.1", "text": "Hijo 6.1", "children": [{"id": "Hijo6.12", "text": "Grado promedio de escolaridad de la población femenina, 0.12%:0.20%"}]}
#                 ]}
#             ]}
#         ]
#     },
#     {
#         "id": "Node 4",
#         "text": "epi_puma_worldclim",
#         "children": [
#             {"id": "Hijo4", "text": "Annual Mean Temperature, 2.050:13.525"},
#             {"id": "Hijo 42", "text": "Annual Mean Temperature, 13.525:15.225"}
#         ]
#     }
# ]

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
    # print("Aquiii =================***********************======")
    # print(selected_names)
    tree_data = [
        {
            "id": "Node 1",
            "text": "epi_puma_censo_inegi_2020",
            'state': {'opened': True},
            "attr": {"nivel": "root", "type": 0},
            "children": [
                {"id": "Node 2", "text": "Node 2", "children": [{"id": "Hijo2", "text": "Grado promedio de escolaridad, 0.00%:0.01%"}]},
                {"id": "node3", "text": "Node 3", "children": [
                    {"id": "Hijo5", "text": "Hijo 5", "children": [{"id": "Hijo5.1", "text": "Población masculina"}]},
                    {"id": "Hijo6", "text": "Hijo 6", "children": [
                        {"id": "Hijo6.1", "text": "Hijo 6.1", "children": [{"id": "Hijo6.12", "text": "Grado promedio de escolaridad de la población femenina, 0.12%:0.20%"}]}
                    ]}
                ]}
            ]
        },
        {
            "id": "Node 4",
            "text": "epi_puma_worldclim",
            "children": [
                {"id": "Hijo4", "text": "Annual Mean Temperature, 2.050:13.525"},
                {"id": "Hijo 42", "text": "Annual Mean Temperature, 13.525:15.225"}
            ]
        }
    ]
    # tree_data = [{"id": "DB",
    #              "text": "DB", 
    #              "children": functionR(DB)} for DB in selected_names]
    return jsonify(tree_data)

@app.route('/process', methods=['POST'])
def process():
    return render_template('arbol.html')#, data=selected_names, D_c=D_c)

@app.route('/select_variables', methods=['POST'])
def select_variables():
    selected_values1 = request.form['selectedVariables1']
    selected_values2 = request.form['selectedVariables2']

    list_db_var = selected_values1.split('\r\n')
    list_db_cov = selected_values2.split('\r\n')

    dict_db_variables = dict_construction(list_db_var)
    dict_db_covariables = dict_construction(list_db_cov)

    all_variables_data = df_construction(dict_db_variables, 'variables')
    all_covariables_data = df_construction(dict_db_covariables, 'covariable')

    all_variables_data['N_v'] = list(map(lambda x: len(set(x)), all_variables_data.iloc[:, -1]))
    all_variables_data['N_vnc'] = [conteo_interseccion(x, list(all_covariables_data.celdas)[0]) for x in list(all_variables_data.celdas)]

    noombre_clase = all_covariables_data.iloc[0, 0]

    return render_template('resDf.html', df_resultado=all_variables_data.to_html(classes="dataframe"), nombre_titulo=noombre_clase)

def conteo_interseccion(l_var, l_cov):
    return sum(1 for var in l_var if var in l_cov)

if __name__ == '__main__':
    app.run(debug=True)