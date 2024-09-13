# Descripción del proyecto
Metaplataforma enfocada en la creación y el análisis de un *ensamble* en el que se cruzan variables de una misma o distintas bases de datos, mediante la presencia o no presencia de las mismas en una malla geográfica con cierta resolución. Esto con el fin de obtener las posibles correlaciones entre un cierto subconjunto de variables del ensamble y otra variable, denominada **clase**, del mismo ensamble construido inicialmente.

## Análisis de los datos:
El análisis se realiza combinando la presencia o ausencia de la clase y las variables evaluadas en alguno de los tipos de resoluciones posibles, que pueden ser: estatal, municipal o AGEB, dentro de la región de toda la República Mexicana. Una vez seleccionada la resolución, es posible elegir las variables disponibles para esa resolución, así como la clase cuya correlación se desea analizar con las otras variables seleccionadas. El objetivo es obtener un resultado cuantitativo de esta relación, medido mediante las métricas de score ($S$) y épsilon ($\epsilon$), definidas por las siguientes fórmulas:

$$S(c|v) = \ln{(\frac{ N_{c\cap v}(N - N_{c}) }{N_{c}(N_{v} - N_{c\cap v})})}    
\hspace{3mm} 
\text{y}
\hspace{3mm}    
\epsilon(c|v) = \frac{ N_{c\cap v} - N_{v}\frac{N_{c}}{N} }{\sqrt{ N_{v}(\frac{N_{c}}{N})(1-\frac{N_{c}}{N}) }}$$


En donde, $N_{c\cap v}$ es la cantidad de conteos (de la resolución escogida) en donde hay presencia tanto de la clase así como de las variables elegidas, $N_c$ es el total de conteos en donde hay presencias de la clase elegida, $N_v$ es el total de conteos donde hay presencia de las variables elegidas y $N$ es el número total de elementos de la resolución elegida dada la resolución (e.g. cantidad de municipios totales en la región de la República Mexicana).


## Interfaz de la plataforma:
Asimismo, se integra un prototipo de interfaz gráfica para el usuario en donde se puede realizar dicho análisis de manera intuitiva mediante la selección de las bases de datos a utilizar dada una cierta resolución, para posteriormente elegir la clase y las variables a analizar en un despliegue de árbol que ordena las variables a partir de la clasificación especificada en la configuración del programa.

### Ejemplo de la interfaz de selección de la clase y las variables

- BD_INEGI
  - Población
    - Población femenina de 1 a 2 años
    - Población femenina de 1 a 2 años
  - Viviendas
    - Viviendas en zonas urbanas
      - Viviendas con acceso a internet
      - Viviendas con linea telefónica
    - Viviendas en zonas rurales
- DB_Worldclim
  - Temperatura media anual
    - Temperatura de 0° a 10°
  - Precipitación promedio anual



Finalmente se obtienen los valores de Score y Épsilon de cada variable en relación a la clase [1], así como los valores de estas métricas para cada unidad de la resolución elegida (e.g. para cada municipio) [2].

### Ejemplo de las tablas de resultados obtenidas en la plataforma:

* Métricas (por variable) para la clase: "*class_1*":

<table style="border-collapse: collapse; width: 50%; margin-left: auto; margin-right: auto;">
<tr>
    <th style="border: 1px solid gray;">Variable</th>
    <th style="border: 1px solid gray;">Score</th>
    <th style="border: 1px solid gray;">Épsilon</th>
</tr>
<tr>
    <td style="border: 1px solid gray;">var_1</td>
    <td style="border: 1px solid gray;">##</td>
    <td style="border: 1px solid gray;">##</td>
</tr>
<tr>
    <td style="border: 1px solid gray;">var_2</td>
    <td style="border: 1px solid gray;">##</td>
    <td style="border: 1px solid gray;">##</td>
</tr>
</table>


* Métricas (por municipio, por ejemplo) para la clase: "*class_1*":
<table style="border-collapse: collapse; width: 60%; margin-left: auto; margin-right: auto;">
<tr>
    <th style="border: 1px solid gray;">Municipio</th>
    <th style="border: 1px solid gray;">Score</th>
    <th style="border: 1px solid gray;">Épsilon</th>
</tr>
<tr>
    <td style="border: 1px solid gray;">mun_1</td>
    <td style="border: 1px solid gray;">##</td>
    <td style="border: 1px solid gray;">##</td>
</tr>
<tr>
    <td style="border: 1px solid gray;">mun_2</td>
    <td style="border: 1px solid gray;">##</td>
    <td style="border: 1px solid gray;">##</td>
</tr>
</table>

Adicionalmente, es posible mostrar solo los resultados más significativos mediante un botón que aplica un filtro, eliminando los resultados con un épsilon menor a 2 en valor absoluto.