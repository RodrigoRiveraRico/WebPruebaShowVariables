## Ejecución de la plataforma
La platforma requiere de Python 3.12 para ser ejecutada.

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

## Descripción del archivo _config.yaml_

* En **plataforma** se indica un nombre para la misma.

  ```yaml
  plataforma:
    name: # Nombre de la plataforma
  ```

* **fuente_de_datos_metadatos** tiene los datos de conexión y parámetros para la consulta de datos.
  
  * Cada llave del diccionario **fuente_de_datos_metadatos** es el nombre de la fuente de datos.
  
    * En caso de que el servidor sea `postgreSQL`: El nombre de la fuente de datos se indica con el nombre de la base de datos.
    
    * En caso de que el servidor sea `endpoints`: Se puede escoger cualquier nombre para identificar dicha fuente de datos.

  * **conexion** es el servidor de donde se extraen los datos: _postgresql_ o _endpoints_.
 
    * Para conexiones con `postgreSQL`:
      
      ```yaml
      fuente_de_datos_metadatos:
        db_name_1:
          conexion: postgresql
          host: # host
          user: # user
          password: # password
          port: # port
          id_column: # id_column_name
          variable_columns:
            - # variable_column_name
            - # variable_column_name
          table: # table
          resoluction:
            res_1:  # resolution_table_name
            res_2:  # resolution_table_name
          categorias:
            ###
      
        db_name_2:
          ###
      ```
     
      * **id_column** es la columna donde está los id's de las variables.
     
      * **variable_columns** es una lista de las columnas que definen a las variables.
        
        El primer elemento de la lista (primera columna) se usará como primer elemento para definir las variables, y así sucesivamente con los demás elementos.

      * **table** es la tabla donde están almacenados los datos.

      * **resolution** es un diccionario que indica la columna donde están las celdas para cada resolución del ensamble.

         La llave correspondiente a la columna donde están las celdas debe estar igualmente indicada en el archivo _./catalogos/catalogo_resoluciones.csv_ con el total de celdas del ensamble.

      * **categorias** es un diccionario con una de las siguientes opciones:

        ```yaml
        categorias:
          archivo: # file.py
        ```
        
        > _file.py_ con script SQL indicando cómo agrupar las variables.

        ```yaml
        categorias:
          columnas:
            - #
            - #
            - #
        ```
        > Lista indicando las columnas con las cuáles agrupar las variables.
        
        > El primer elemento de la lista (primera columna) se usará como primer elemento para agrupar las variables, y así sucesivamente con los demás elementos.

        ```yaml
        categorias:
          Null
        ```
        
        > _Null_ en caso de no tener las dos opciones anteriores.

    * Para conexiones con `endpoints`:
   
      ```yaml
      fuente_de_datos_metadatos:
        data_source_name_1:
          conexion: endponits
          variables: # url
          get_data: # url

        data_source_name_2:
          ###
      ```
 
      * En **variables** se indica la URL al endpoint _/variables_

      * En **get_data** se indica la URL al endpoint _/gat-data_
  

## Ejemplo del archivo _config.yaml_

A continuación se tiene un ejemplo de cómo escribir el archivo de configuración `yaml` con una fuente de datos de `postgreSQL` y otra en `endpoints`, mostrando así que se pueden combinar fuentes de datos provenientes de diferentes servidores en la misma plataforma.

```yaml
plataforma:
  name: Configuracion de ejemplo

fuente_de_datos_metadatos:
  inegi_db: 
    conexion: postgresql
    host: ****
    user: ****
    password: ****
    port: ****
    id_column: id
    variable_columns:
      - name
      - interval
    table: covariable
    resolution:
      mun: cells_mun
      state: cells_state
    categorias:
      archivo: inegi_db_sql.py

  INEGI (endpoints):
    conexion: endpoints
    variables: http://.../variables
    get_data: http://.../get-data
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
