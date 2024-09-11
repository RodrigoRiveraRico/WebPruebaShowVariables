// Construcción del jstree de un solo nivel:
function updateDBSelect(){
    var res = ''
    var DBs_selected_res = []; // Lista de bases de datos corresponcientes a la resolución seleccionda.
    res = document.getElementById("res_selector").value;   // String con el nombre de la resolución selecionada.            
    let DBs_res = Dict_res[res]; 

    let nodos = DBs_res.map((item, index)=> ({  // Se construyen los nodos con los nombres de las BD correspondientes a la resolución seleccionada.
        "text": item, // El texto del nodo
        "id": `nodo_${index + 1}`, // Asignar un id único
        "state": { "selected": true } // Marcar como seleccionado desde el inicio
    }));

    console.log(DBs_res);

    // Destruir el jstree antes de volverlo a inicializar (si es que ya se inicializó anteriormente)
    if ($('#Res_tree').jstree(true)) {   // Este if es para actualizar el arbol cuando se selecciona una resolución distinta.
        $('#Res_tree').jstree(true).destroy();
    }

    // Construir el árbol con la resolución seleccionada:

    $('#Res_tree').jstree({ 'core': { 'data': nodos, 
                                        'themes': {   /// Cambiar el tema
                                            'name': 'proton', // nombre del tema
                                            'responsive': true,
                                            'dots': true, // mostrar puntos entre nodos
                                            'icons': true, // mostrar iconos junto a los nodos
                                            'state': { checked: true }
                                        } },
                                "checkbox" : {  // habilitar los checkboxes
                                            "keep_selected_style" : false,
                                            "selected" : true 
                                            },
                                "plugins" : [ "checkbox"]
                            });


    $('#Res_tree').on("changed.jstree", function (e, data) {   // e = evento ("changed" en este caso)
        DBs_selected_res = data.selected.map(function(node_id) { //data.selected es una lista de los IDs de los nodos seleccionados.
            return data.instance.get_node(node_id).text;
        });; // Actualiza la lista con los nodos seleccionados (toma los texts a partir de los IDs de los nodos seleccionados.)
        console.log(DBs_selected_res)
    });
    console.log('fuera del changed:',DBs_selected_res)


    // Enviar DBs_selected_res y res al main.py:
    document.getElementById('selectDB_res').addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Convertir las listas un array para enviarlo como JSON
        DBs_selected_res = Array.from(DBs_selected_res);

        // Enviar el Array mediante AJAX
        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ DBs_selected_res: DBs_selected_res, res : res})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.redirect;  // Redirige a la nueva URL
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });

};

// Esto es para que se carguen las opciones desde que se carga la página --
document.addEventListener('DOMContentLoaded', (event) => {
updateDBSelect();
});