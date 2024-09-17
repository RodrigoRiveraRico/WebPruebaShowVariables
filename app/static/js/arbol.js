// Aquí se construyen los dos árboles (#tree de las variables y #tree2 para seleccionar la clase): 
$(function () {
    $.getJSON('/tree_data', function (data) {
        $('#tree').jstree({ 'core': { 'data': data,  // Arbol de las variables.
                                    'themes': {   /// Cambiar el tema
                                        'name': 'proton', // nombre del tema
                                        'responsive': true,
                                        'dots': true, // mostrar puntos entre nodos
                                        'icons': false // mostrar iconos junto a los nodos
                                    } },
                            "checkbox" : {
                                        "keep_selected_style" : false,
                                        },
                            "plugins" : [ "checkbox", "search"]
                        });
        $('#tree2').jstree({ 'core': { 'data': data,   // Arbol de la clase.
                                    'themes': {   /// Cambiar el tema
                                        'name': 'proton', // nombre del tema
                                        'responsive': true,
                                        'dots': true, // mostrar puntos entre nodos
                                        'icons': false // mostrar iconos junto a los nodos
                                    },
                                    // "multiple": false,
                                    // "check_callback": true,
                                    },
                            "checkbox" :{
                                        "tie_selection": false,
                                        // "keep_selected_style" : true
                                        "three_state": false, // desactiva checkboxes tri-estados
                                        "cascade": "none" // evita la selección automática de nodos hijos/padres
                                        },
                            "plugins" : ["checkbox", "search"]
                        });
    });
});


// === Funciones para realizar la búsqueda en los árboles  !!!(Comentar este bloque de código si se quiere deshabilitar esa función).
$('#search-input').on('keyup', function() {
    var searchString = $(this).val();  // Obtener el valor del input
    $('#tree').jstree('search', searchString);  // Ejecutar la búsqueda
});
$('#search-input2').on('keyup', function() {
    var searchString = $(this).val();  // Obtener el valor del input
    $('#tree2').jstree('search', searchString);  // Ejecutar la búsqueda
});
// ===.


$('#tree2').on("click.jstree", ".jstree-anchor", function (event) {
    // Evita que el checkbox se seleccione si el clic no es en el checkbox
    if (!$(event.target).hasClass('jstree-checkbox')) {
        event.stopImmediatePropagation();
        event.preventDefault();
    }
});

// En esta función se maneja la interacción con los árboles: 
$(function () {

    // Con checkbox:
    var selectedNodes = []
    var selectedNodes2 = []

    //// Manejar cuando los cambios de selección en cada árbol:

    // Árbol 1 (de las variables)
    $('#tree').on("changed.jstree", function (e, data) {   // e = evento ("changed" en este caso)
        selectedNodes = filtrarYTransformar(data.selected); // Actualiza la lista con los nodos seleccionados
    });


    // Árbol 2 (de la clase)

    let isHandlingEvent = false;
    $('#tree2').on("check_node.jstree uncheck_node.jstree", function (e, data) {
        if (isHandlingEvent) return;  // Evitar recursión de la llamada de la función checknode y uncheck all.
        isHandlingEvent = true;

        if (e.type === 'check_node') {
            $('#tree2').jstree(true).uncheck_all(); // Deselecciona todos los nodos
            $('#tree2').jstree(true).check_node(data.node.id); // Selecciona el nodo actual
        }

        let checkedNodes = $('#tree2').jstree("get_checked", true) // Obtiene los nodos checkeados
            .map(node => node.id); // Extrae los IDs de los nodos
        selectedNodes2 = filtrarYTransformar(checkedNodes); // Filtra y transforma los IDs, actualizando la lista                                
        isHandlingEvent = false;
    });

    // Envío de las listas de las variables y la clase seleccionada:

    document.getElementById('selectVariablesForm').addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Convertir las listas un array para enviarlo como JSON
        selectedNodes = Array.from(selectedNodes);
        selectedNodes2 = Array.from(selectedNodes2);

        // Enviar el Array mediante AJAX
        fetch('/select_variables', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selectedNodes: selectedNodes, selectedNodes2: selectedNodes2 })
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


    // Funciones auxiliares:

    function transformarCadena(cadena) {
        /**
         * Transforma la sintaxis de los ids a la que utilizamos en la ruta de python.
         * @param {string} cadena - Cadena a transformar.
         */
        var regex = /__(.*?)__/g;
        var match;
        var fragmentos = [];

        // Recorremos todas las coincidencias de la expresión regular en la cadena
        while ((match = regex.exec(cadena)) !== null) {
            // match[1] contiene el fragmento entre __
            fragmentos.push(match[1]);
        }

        // Se unen todos los fragmentos con ':'
        return fragmentos.join(':');
    }

    // Función para filtrar y transformar IDs
    function filtrarYTransformar(nodes) {
        return nodes
            .filter(cadena => cadena.startsWith("__"))   // Con esto obtiene el nombre de la base de datos y de las variables.
            .map(transformarCadena);   // Transforma la sintaxis de los ids a la que utilizamos en la ruta de python.
    }

    $('#sendButton').show();
});
