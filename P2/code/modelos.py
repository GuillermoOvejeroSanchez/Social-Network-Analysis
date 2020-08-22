import networkx as nx
import random

#Funcion para generar una red aleatoria, es decir,modelo de Erdös-Renyi. 
#Le pasamos dos arguemtnos, por una lado el tamaño de la red a generar (N) y por otro la probalidad con la que se enlazan dos nodos (p).
def random_graph(N,p):
    G = nx.Graph()
    G.add_nodes_from(range(N))
    #Declaramos un grafo vacio y lo llenamos con nodos sin enlazar

    for nodo1 in range(N): #cogemos un nodo 
        for nodo2 in range(nodo1 + 1, N): # desde el siguiente nodo a nodo1 buscamos nodos que se puedan enlazar con nodo1
            random_num = random.random() # generamos un numero aleatorio [0.0, 1.0)
            if random_num <= p: # si el numero aleatorio generado es menor o igual que p nodo1 y nodo2 se pueden enlazar
                G.add_edge(nodo1, nodo2) #creamos dicho enlace en el grafo

    return G

def barabasi_albert(nodos, m):
    m0 = m + 1
    t = nodos - m0
    G = nx.complete_graph(m0) #Creamos el grafo con una distribucion inicial de m0 nodos con al menos un enlace cada nodo

 
    '''
    --------------------------------------------------------------------------------------------------------------------------------------------------
                                         PREPROCESAMIENTO
    --------------------------------------------------------------------------------------------------------------------------------------------------
    '''
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
        '''
        PARA AGRERAR ARISTAS AL NUEVO NODO USAREMOS EL METODO DE PROBABILIDADES ACUMULADAS
        Implementaremos la idea de conexion preferencial mediante este metodo. 

        Se genera un numero aleatorio [0.0, 1)
        Usaremos una nueva metrica llamada probabilidad acumulada que es la suma de las probabilidades anteriores

        Con estos dos valores podremos implementar la conexion preferencial ya que cuato mayor sea la probabilidad 
        acumulada mas conexiones tendrá. Con una probabilidad acumulada alta la ventana de posibulidades para ser escogida es mayor, en caso 
        contrario si la probabilidad acumulada es baja la venta de posibilidades es mas pequeña haciendo que sea menos probable que se escoja ese 
        nodo. 

        Ejemplo: 
        probabilidades = [0.2, 0.3, 0.5]
        probabilidadAcumulada = [0.2, 0.5, 1.0]

        Numero aleatorio de [0.0, 1.0)
        n = 0.4

        ventanas: 
        0.2: [0.0, 0.2]
        0.5: [0.0, 0,5]
        1.0: [0.0, 1.0]

        Cuanto mas grande sea la ventana, mas probable es que el numero aleatorio caiga dentro de esa ventana 
        '''

        #Vamos a crear una lista de probabilidades acumuladas, la cual contendrá tuplas. 
        #Cada tupla, tendra id del nodo y la probabilidad acumulada (id,probAcumulada)
        probAcumulada = [] #lista vacia
        aux = 0
        for idNodo, probabilidad in probConexion.items(): 
            nodo = (idNodo, aux + probabilidad) #creamos un elemento de la lista con la informacion necesaria 
            probAcumulada.append(nodo)

            aux += probabilidad #actualizamos lo anterior con lo actaul para la siguiente iteracion 
    
    
    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #                                              CREACION DE CONEXIONES
    #--------------------------------------------------------------------------------------------------------------------------------------------------
    

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
            
            print(conexiones)   
            if conexiones < 501 and conexiones % 25 == 0 or (conexiones < 20 and conexiones % 5 == 0):
                nx.write_edgelist(G, '../graphs/barabasi-albert/steps/ba_steps_{:03d}.csv'.format(source), delimiter=",", data=True)
    
    return G
