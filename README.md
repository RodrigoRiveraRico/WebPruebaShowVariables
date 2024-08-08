## Ejecución de la plataforma

### WINDOWS

```CMD
set FLASK_CONFIG_FILE=config.yaml
set SECRET_KEY=secret_key_de_tu_entorno_de_ejecucion

flask --app run run --port=4000 --host=0.0.0.0
```

### LINUX:

```bash
export FLASK_CONFIG_FILE=config.yaml
export SECRET_KEY='secret_key_de_tu_entorno_de_ejecucion'

flask --app run run --port=4000 --host=0.0.0.0
```

> host=0.0.0.0 para que la plataforma se pueda visualizar desde cualquier dispositivo conectado a la red del servidor donde se ejecuta la plataforma.

> _config.yaml_ debe estar ubicado en _./configuraciones_db_

## Ejemplo del archivo _config.yaml_

* En **plataforma** se inidica un nombre para la misma.
  
* **variable_columns** es una lista de las columnas que definen a las variables.
  
* **table** es la tabla donde están almacenados los datos.
  
* **resolution** indica la columna donde están las celdas para cada resolución del ensamble.
  
  La llave correspondiente a la columna donde están las celdas debe estar igualmente indicada en el archivo _./catalogos/catalogo_resoluciones.csv_ con el total del ensamble.
  
* **categorias**: una de las siguientes:
  
  * Diccionario key='archivo', value: file.py con sql indicando cómo agrupar las variables.
    
  * Diccionario key='columnas', value: lista indicando las columnas de la base de datos con las cuáles agrupar de forma ordenada.
  
  * _Null_ en caso de no tener las dos opciones anteriores.

```yaml
plataforma:
  name: Configuracion de default (INEGI)

fuente_de_datos_metadatos:
  epi_puma_censo_inegi_2020: 
    host: ****
    user: ****
    password: ****
    port: ****
    variable_columns:
      - name
      - interval
    table: covariable
    resolution:
      mun: cells_mun
      state: cells_state
      ageb: cells_ageb
    categorias: 
      # archivo: file.py
      # columnas :
      #   - col_1
      #   - col_2
      # Null
```

## Ejemplo del archivo _file.py_ indicado en _config.yaml_

* _file.py_ debe estar ubicado en _./configuraciones_db_

* En la variable _col_ se indica la colmuna (de la base de datos) a tratar.
  
* En _txt_ se construye la consulta SQL tal que organiza las variables según como el usario las requiera.

```python
col = 'name'

txt = f'''
CASE 
    WHEN {col} LIKE 'Grado promedio%' THEN CONCAT('estudios',', ','escolaridad') 
    WHEN {col} LIKE '%afiliada%servicios%' THEN CONCAT('salud',', ','servicios salud')
    WHEN {col} LIKE '%condici_n mental%' or {col} LIKE '%discapacidad%' or {col} LIKE '%limitaci_n%' THEN CONCAT('salud',', ','discapacidad')
    WHEN {col} LIKE '%censales%referencia%' or {col} LIKE '%viviendas particulares%' or {col} LIKE '%religi_n%' or {col} LIKE '%a_os%' or {col} LIKE '%poblaci_n nacida%entidad%' THEN CONCAT('personas',', ','población')
    WHEN {col} LIKE '%poblaci_n femeninca%' or {col} LIKE '%pobalci_n masculina' THEN CONCAT('personas',', ','genero')
    WHEN {col} LIKE '%viviendas particulares%' THEN CONCAT('vivienda',', ','vivienda1')
    WHEN {col} LIKE '%viviendas particulares habitadas que no%' THEN CONCAT('vivienda',', ','vivienda2')
    ELSE CONCAT('Otros')
END
'''
```
