<h1 align="center">Chilam Project</h1>

<p align="center">~ Centro de Ciencias de la Complejidad, UNAM ~</p>

<br/>

**Para leer la descripción del proyecto, entrar [aquí](Description.md).**

A continuación se detallan los aspectos técnicos de la plataforma.


## Contenido

* [Ejecución de la plataforma](#ejecución-de-la-plataforma)

  * [WINDOWS](#windows)

  * [LINUX](#linux)

* [Descripción del archivo config.yaml](#descripción-del-archivo-configyaml)

* [Ejemplo del archivo config.yaml](#ejemplo-del-archivo-configyaml)

* [Estructura de los datos almacenados en postgreSQL](#estructura-de-los-datos-almacenados-en-postgresql)

* [Estructura de los datos almacenados en endpoints](#estructura-de-los-datos-almacenados-en-endpoints)

* [Ejemplo del archivo file.py indicado en config.yaml](#ejemplo-del-archivo-filepy-indicado-en-configyaml)

* [Ejemplo del archivo catalogo_resoluciones.csv](#ejemplo-del-archivo-catalogo_resolucionescsv)

## Ejecución de la plataforma

La plataforma fue probada con Python 3.11

### WINDOWS

```CMD
set FLASK_CONFIG_FILE=config.yaml
set SECRET_KEY=secret_key_de_tu_entorno_de_ejecucion

flask --app run run --port=4000 --host=0.0.0.0
```

### LINUX

```bash
export FLASK_CONFIG_FILE=config.yaml
export SECRET_KEY='secret_key_de_tu_entorno_de_ejecucion'

flask --app run run --port=4000 --host=0.0.0.0
```

> host=0.0.0.0 para que la plataforma se pueda visualizar desde cualquier dispositivo conectado a la red del servidor donde se ejecuta la plataforma.

## Descripción del archivo _config.yaml_

* El archivo _config.yaml_ debe estar ubicado en _./configuraciones_db_

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
          resolution:
            res_1:  # resolution_column_name
            res_2:  # resolution_column_name
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

## Estructura de los datos almacenados en `postgreSQL`

Las siguientes tablas ejemplifican cómo se estructuran esencialmente los datos en `postgreSQL` para incorporarlos en la plataforma.

* Tipo de dato:

  | columna | tipo |
  |:--:|:--:|
  | **id** | integer not null |
  | **name** | text |
  | **interval** | text |
  | **cells_mun** | character varying[] |
  | **cells_state** | character varying[] |

* Estructura:

  | id | name | interval | cells_mun | cells_state |
  |:--:|:--:|:--:|:--:|:--:|
  | 1 | Población Total | 100:200 | [01432, 02345, 04112] | [01, 02, 04] | 
  | 2 | Población Total | 200:300 | [02243, 10353, 11221] | [02, 10, 11] | 
  | 3 | Población Total | 300:400 | [10013, 10111, 10222] | [10] | 

En el archivo _config.yaml_ se colocan los siguientes parámetros para el caso de la tabla anterior con nombre _covariable_:

```yaml
id_column: id
variable_columns:
  - name
  - interval
table: covariable
resolution:
  mun: cells_mun
  state: cells_state
```

Las llaves en el diccionario _resolution_ son:

* **mun**, que hace referencia a una resolución municipal.

* **state**, que hace referencia una resolución estatal.

Estas llaves tienen que estar indicadas en el archivo _./catalogos/catalogo_resoluciones.csv_ [(Ver ejemplo)](#ejemplo-del-archivo-catalogo_resolucionescsv)

## Estructura de los datos almacenados en `endpoints`

Los datos almacenados en `endpoints` siguen la estructura definida en este [GitHub][conabio].

[conabio]: https://github.com/CONABIO/species_v3.0

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

## Ejemplo del archivo _catalogo\_resoluciones.csv_ 

* Este archivo debe estar ubicado en _./catalogos_

* Contiene las resoluciones indicadas en _config.yaml_ para conexiones con `postgreSQL`.

* Contiene también las resoluciones definidas en los `endpoints`.

```
resolution,N
mun,2446
state,32
```

En el ejemplo anterior se tiene la resolución _mun_ (que hace referencia a resoluciones municipales) y _state_ (que hace referencia a resoluciones estatales) con su respectivo total de celdas.

* La resolución _mun_ tiene un total de N = 2446 celdas.

* La resolución _state_ tiene un total de N = 32 celdas.
