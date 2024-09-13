# Descripción del proyecto

Plataforma centralizada para el *Laboratorio para la Simulación de Sistemas Complejos Adaptativos (CHILAM)* [(Sitio Web)](https://chilam.c3.unam.mx/) enfocada en la creación y el análisis de un *ensamble* en el que se cruzan variables de una misma o distintas bases de datos, mediante la presencia o no presencia de las mismas en una malla geográfica con cierta resolución. Esto con el fin de obtener las posibles correlaciones entre un cierto subconjunto de variables del ensamble y otra variable, denominada **clase**, del mismo ensamble construido inicialmente.

## Análisis de los datos:
El análisis se realiza combinando la presencia o ausencia de la clase y las variables evaluadas en alguno de los tipos de resoluciones posibles, que pueden ser: estatal, municipal o AGEB, dentro de la región de toda la República Mexicana. Una vez seleccionada la resolución, es posible elegir las variables disponibles para esa resolución, así como la clase cuya correlación se desea analizar con las otras variables seleccionadas. El objetivo es obtener un resultado cuantitativo de esta relación, medido mediante las métricas de score y épsilon, definidas por las siguientes fórmulas:

$$S(c|v) = \ln{(\frac{ N_{c\cap v}(N - N_{c}) }{N_{c}(N_{v} - N_{c\cap v})})}$$
y
$$\epsilon(c|v) = \frac{ N_{c\cap v} - N_{v}\frac{N_{c}}{N} }{\sqrt{ N_{v}(\frac{N_{c}}{N})(1-\frac{N_{c}}{N}) }}$$


En donde, $N_{c\cap v}$ es la cantidad de conteos (de la resolución escogida) en donde hay presencia tanto de la clase así como de las variables elegidas, $N_c$ es el total de conteos en donde hay presencias de la clase elegida, $N_v$ es el total de conteos donde hay presencia de las variables elegidas y $N$ es el número total de elementos de la resolución elegida dada la resolución (e.g. cantidad de municipios totales en la región de la República Mexicana).


## Interfaz de la plataforma:
Asimismo, se integra un prototipo de interfaz gráfica para el usuario en donde se puede realizar dicho análisis de manera intuitiva mediante la selección de las bases de datos a utilizar, la resolución, así como la clase y las variables a analizar, para finalmente obtener los valores de Score y Épsilon de cada variable en relación a la clase, así como los valores de estas métricas para cada unidad de la resolución elegida (e.g. para cada estado).