var selectedNames = [];

function showSuggestionsClick() {
    var input = document.getElementById("nameInput");
    var value = input.value.trim().toLowerCase();
    var suggestionsContainer = document.getElementById("suggestions");
    suggestionsContainer.innerHTML = "";
    
    var matches = suggestions.filter(function(suggestion) {
        return suggestion.toLowerCase().startsWith(value);
    });

    matches.forEach(function(suggestion) {
        var suggestionElement = document.createElement("div");
        suggestionElement.textContent = suggestion;
        suggestionElement.onclick = function() {
            input.value = suggestion;
            suggestionsContainer.innerHTML = "";
        };
        suggestionsContainer.appendChild(suggestionElement);
    });
    document.getElementById('suggestions').style.display = 'block';
}

function showSuggestions() {
    var input = document.getElementById("nameInput");
    var value = input.value.trim().toLowerCase();
    var suggestionsContainer = document.getElementById("suggestions");
    suggestionsContainer.innerHTML = "";

    if (value === "") return;

    var matches = suggestions.filter(function(suggestion) {
        return suggestion.toLowerCase().startsWith(value);
    });

    matches.forEach(function(suggestion) {
        var suggestionElement = document.createElement("div");
        suggestionElement.textContent = suggestion;
        suggestionElement.onclick = function() {
            input.value = suggestion;
            suggestionsContainer.innerHTML = "";
            suggestionsContainer.style.display = 'none';
        };
        suggestionsContainer.appendChild(suggestionElement);
    });
    suggestionsContainer.style.display = 'block';
}

function addName() {
    var nameInput = document.getElementById("nameInput");
    var name = nameInput.value.trim();
    if (name && !selectedNames.includes(name)) {
        selectedNames.push(name);
        updateSelectedNames();
        sendNameToServer(name);
    }
    nameInput.value = "";
}

function except_fun(){
    if (selectedNames.length == 0){
        alert('No se han seleccionado bases de datos.')
        return false
    }
    return true
}

function updateSelectedNames() {
    var selectedNamesList = document.getElementById("selectedNames");
    selectedNamesList.innerHTML = "";
    selectedNames.forEach(function(name) {
        var li = document.createElement("li");
        li.textContent = name;
        selectedNamesList.appendChild(li);
    });
    document.getElementById("selectedNamesInput").value = JSON.stringify(selectedNames);
}

function sendNameToServer(name) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/add_name", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Actualizar la lista de nombres seleccionados desde la respuesta del servidor
            selectedNames = JSON.parse(xhr.responseText).selected_names;
            updateSelectedNames();
        }
    };
    xhr.send("name=" + encodeURIComponent(name));
}