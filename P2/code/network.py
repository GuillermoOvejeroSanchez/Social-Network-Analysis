import click
import networkx as nx
import modelos
import random

@click.group()
def cli():
    """
    Simple CLI for producing network models
    """


@cli.command()
@click.option('--nodos', default=500, help='number of nodes')
@click.option('--m', default=3, help='indicates the m value, must be m < n')

def barabasi_albert(nodos,m):
    click.echo('generating barabasi albert model with n = {}, m = {}'.format(nodos,m))
    m0 = m + 1
    t = nodos - m0
    G = nx.complete_graph(m0) #Creamos el grafo con una distribucion inicial de m0 nodos con al menos un enlace cada nodo
    for i in range (m0, nodos): #añadimos los N - n0 nodos restantes
        G.add_node(i) # añadimos el nodo nuevo queremos conecar
        sumaGradosNodos = 0

        for nodo in range (0, i): 
            sumaGradosNodos += G.degree(nodo) 
        #Sumamos los grados de todos los nodos que forman la red en este momento, para posteriormente calcular formula de la probablidad de conexion 
        probConexion = {} #Creamos un diccionario donde guardar la probabilidad de cada nodo para crear una nueva conexion con el nodo i 
        #Esto metodo es conocido como Conexion preferencial ya que se conectara con nodos que tenga mas conexiones 
        #probConexion -> clave: id del nodo, valor: probalid

        gradosNodos = nx.degree(G) #Sacamos la lista con los grados de cada nodo
        #Llenamos el diccionario con las probabilidades de cada nodos que hay hasta este momento con la formula: 
        #Pi = ki / SUM kj 
        #Pi es la probabilidad de que uno de los enlaces se conecte al nodo nuevo 
        # donde ki es el grado del nodo existente 
        #denominador suma de los grados de la red hasta este momento
        for j in range (0,i):
            probConexion[j] = (float)(gradosNodos[j])/sumaGradosNodos

        #Vamos a crear una lista de probabilidades acumuladas, la cual contendrá tuplas. 
        #Cada tupla, tendra id del nodo y la probabilidad acumulada (id,probAcumulada)
        probAcumulada = [] #lista vacia
        aux = 0
        for idNodo, probabilidad in probConexion.items(): 
            nodo = (idNodo, aux + probabilidad) #creamos un elemento de la lista con la informacion necesaria 
            probAcumulada.append(nodo)

            aux += probabilidad #actualizamos lo anterior con lo actaul para la siguiente iteracion 

    #Ahora hay que hacer m conexiones, m aristas, con m nodos. Basandonos en los datos extraidos anteriormente
        conexiones = 0 
        nodosAdded = [] #Lista de nodos selccionados para conectarlos con el nuevo nodo

        while(conexiones < m): 
            n = random.random() 
            actual = 0

            while(actual < i and probAcumulada[actual][1] < n): # No nos pasamos del nuevo nodo y la probabilidad acumulado es menor que la n, entonces pasamos al suiente nodo candidato 
                actual += 1
            
            idDestino = probAcumulada[actual][0] # extreamos el id del nodo seleccionado para formar la conexion 

            #Vamos a comprobar si idDestino no tiene conexion con el nodo nuevo 
            if idDestino not in nodosAdded: 
                nodosAdded.append(idDestino) # lo metemos en la lista de nodos selecionados 
                G.add_edge(i,idDestino) #añadimos la conexional grafo 
                conexiones += 1
                       
        if i < 501 and i % 25 == 0 or (i < 20 and i % 5 == 0):
            nx.write_edgelist(G, '../graphs/barabasi-albert/steps/ba_steps_{:03d}.csv'.format(i), delimiter=",", data=True)
                
    nx.write_edgelist(G, '../graphs/barabasi-albert/ba_{}_{}.csv'.format(m,nodos), delimiter=",", data=True)
    return G


@cli.command()
@click.option('--n', default=500, help='number of nodes')
@click.option('--p', default=0.01, help='indicates the p value, probability')
@click.option('--total', default=1, help='indicate how many random graphs do you want')

def erdos_renyi(n,p,total):
    click.echo('generating {} erdos renyi model(s) with n = {}, p = {}'.format(total,n,p))
    for i in range(total):
        er = modelos.random_graph(n,p)
        nx.write_edgelist(er, '../graphs/erdos-renyi/erdos_renyi_{}_n{}_p{}.csv'.format(i,n,p), delimiter=",", data=True)

if __name__ == "__main__":
    cli()