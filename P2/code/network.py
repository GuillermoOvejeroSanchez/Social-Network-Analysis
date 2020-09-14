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
@click.option('--n', default=500, help='number of nodes')
@click.option('--m', default=3, help='indicates the m value, must be m < n')

def barabasi_albert(n,m):
    """Generates a barabasi albert graph given the number of nodes and the m value"""

    click.echo('generating barabasi albert model with n = {}, m = {}'.format(n,m))
    m0 = m + 1
    t = n - m0
    G = nx.complete_graph(m0) 
    for i in range (m0, n): 
        G.add_node(i) 
        sumaGradosNodos = 0

        for nodo in range (0, i): 
            sumaGradosNodos += G.degree(nodo) 
       
        probConexion = {}
        gradosNodos = nx.degree(G) 
        for j in range (0,i):
            probConexion[j] = (float)(gradosNodos[j])/sumaGradosNodos

        probAcumulada = [] 
        aux = 0
        for idNodo, probabilidad in probConexion.items(): 
            nodo = (idNodo, aux + probabilidad) 
            probAcumulada.append(nodo)
            aux += probabilidad 

        conexiones = 0 
        nodosAdded = [] 
        while(conexiones < m): 
            num = random.random() 
            actual = 0
            while(actual < i and probAcumulada[actual][1] < num):  
                actual += 1

            idDestino = probAcumulada[actual][0] 
            if idDestino not in nodosAdded: 
                nodosAdded.append(idDestino)  
                G.add_edge(i,idDestino)
                conexiones += 1
                       
        if i < 501 and i % 25 == 0 or (i < 20 and i % 5 == 0):
            nx.write_multiline_adjlist(G, '../graphs/barabasi-albert/steps/ba_n_{}_m_{}_steps_{:03d}.csv'.format(n,m,i), delimiter=",")
                
    nx.write_multiline_adjlist(G, '../graphs/barabasi-albert/ba_{}_{}.csv'.format(m,n   ), delimiter=",")
    return G


@cli.command()
@click.option('--n', default=500, help='number of nodes')
@click.option('--p', default=0.01, help='indicates the p value, probability')
@click.option('--total', default=1, help='indicate how many random graphs do you want')

def erdos_renyi(n,p,total):
    """ Generates an erdos renyi graph, also called random graph, given the number of nodes 'n' the probability 'p' and the total of graphs to generate with those variables"""
    
    click.echo('generating {} erdos renyi model(s) with n = {}, p = {}'.format(total,n,p))
    for i in range(total):
        G = nx.Graph()
        G.add_nodes_from(range(n))
        #Declaramos un grafo vacio y lo llenamos con nodos sin enlazar

        for nodo1 in range(n): #cogemos un nodo 
            for nodo2 in range(nodo1 + 1, n): # desde el siguiente nodo a nodo1 buscamos nodos que se puedan enlazar con nodo1
                random_num = random.random() # generamos un numero aleatorio [0.0, 1.0)
                if random_num <= p: # si el numero aleatorio generado es menor o igual que p nodo1 y nodo2 se pueden enlazar
                    G.add_edge(nodo1, nodo2) #creamos dicho enlace en el grafo


        #nx.write_edgelist(er, '../graphs/erdos-renyi/erdos_renyi_{}_n{}_p{}.csv'.format(i,n,p), delimiter=",", data=True)
        nx.write_multiline_adjlist(G, '../graphs/erdos-renyi/erdos_renyi_{}_n{}_p{}.csv'.format(i,n,p), delimiter=",")

if __name__ == "__main__":
    cli()