## 1. Desarrollo de modelos
- [x] 1.1 Creacion de 2 redes iguales de cada tipo
- [x] 1.2 Actualizar en cada paso de simulacion (Barabasi-Albert)
- [x] 1.3 Etapas: subcrítica p < 1/N, crítica p = 1/N, supercrítica p < 1/N y conectada p > ln(N)/N.
- [x] 1.4 CLI creado para la generacion de grafos
- [x] 1.5 Manual de uso de CLI (mas abajo)
## 2. Verificacion de propiedades de las redes, segun su modelo teorico
- [x] 2.1 Visualizaciones de los pasos del modelo Barabasi-Albert
- [x] 2.2 Visualizaciones de las diferentes regiones
- [x] 2.3 Verificar propiedades de los mismos modelos, ver diferencias entre modelos
## 3. Estudio de la red de la practica 1, Actores-Peliculas
- [x] 3.1 A que modelo se aproxima mas? Comparacion de ambas redes


## Manual uso de CLI
#### network.py
Ejecutamos el CLI de python desde donde queramos que se guarden los grafos generados, en este caso sera desde la subcarpeta 'graphs/'

![Network Help](img/networkHelp.PNG)

Tenemos 2 opciones para generar modelos de grafo, barabasi-albert y erdos-renyi

![](img/networkUsage.PNG)

Y dependiendo del modelo, unos parametros diferentes,En Barabasi Albert tenemos dos parametros numero de nodos (ej --n 500) y el valor de nodos iniciales m (ej --m 3)

Erdos Renyi tendremos el numero de nodos (ej --n 500) probabilidad (ej --p 0.001) y el numero total de grafos a generar (ej --total 10)

En ambos podemos no especificar nada y se generara un grafo con sus parametros por defecto, (n=500, m=3, p=0.001 y total=1)


![](img/generacionRedes.png)
