transiciones = "abcdefghijklmnopqrstuvwxyz"

def LeerDatosGenrales():
    nroEstados = int(input())
    nroTransiciones = int(input())
    return [nroEstados, nroTransiciones]


def LeerTransiciones():
    transiciones = input().split()
    return transiciones


def GenerarAutomata(nroEstados):
    automata = {}
    matriz = {}
    listaEstados = []
    for i in range(nroEstados):
        transiciones = LeerTransiciones()
        AgregarAListaEstados(listaEstados, transiciones)

        CrearEstado(transiciones, automata, matriz, i)

    if len(listaEstados) < nroEstados:
        return False         

    return automata, matriz,listaEstados

def CrearEstado(transiciones, automata, matriz, estado):
    estadoCreado, transicionesMatriz = CrearTransiciones(transiciones, estado)
    automata[str(estado)] = estadoCreado
    matriz[str(estado)] = transicionesMatriz
    
    return automata


def AgregarAListaEstados(arreglo, transiciones):
    for i in transiciones:
        if i not in arreglo:
            arreglo.append(i)


def CrearTransiciones(transicionesEstado, estado):
    result = {}
    transicionesMatriz = {}
    abecedario = "abcdefghijklmnopqrstuvwxyz"
    # print(estado)
    # print('\n')

    for i in range(len(transicionesEstado)):
        letra = abecedario[i]
        result[letra] = str(transicionesEstado[i])
        
        if str(estado) == str(transicionesEstado[i]): 
            transicionesMatriz[str(transicionesEstado[i])] = 20

        elif len(str(estado).split(',')) > len(str(transicionesEstado[i]).split(',')):
            transicionesMatriz[str(transicionesEstado[i])] = 1

        else :
            transicionesMatriz[str(transicionesEstado[i])] = 2


    return result, transicionesMatriz


def CrearCombinaciones(iterable, r):
    pool = tuple(iterable)
    n = len(pool)

    if r > n:
        return

    indices = list(range(r))
    yield list(tuple(pool[i] for i in indices))

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return

        indices[i] += 1

        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1

        yield list(tuple(pool[i] for i in indices))


def AgregarNewEstados(automata, matriz, nroEstados, estadosIniciales):
    estados =  []

    for i in range(2,nroEstados+1):
        estados.extend(CrearCombinaciones(estadosIniciales, i))

    AgregarValores(estados, automata, matriz)


def AgregarValores(estados, automata, matriz):
    for estado in estados:
        i=-1
        estado = ','.join(estado)
        while estado[i] != ",":
            i-=1
    
        estadoUnico = estado[(i+1):]
        oldEstado = estado[:i]

        transiciones, transicionesMatriz = HallarTransiciones(automata, estadoUnico, oldEstado, estado)

        automata[estado] = transiciones
        matriz[estado] = transicionesMatriz



def HallarTransiciones(automata, estadoUnico, oldEstado, estado):
    result = {}
    resultMatriz = {}
    abecedario = "abcdefghijklmnopqrstuvwxyz"
    temp = automata[estadoUnico]
    temp2 = automata[oldEstado]


    for i in range(len(automata['1'])):
        letra = abecedario[i]
        tempTran = temp[letra]
        temp2Tran = temp2[letra]

        tempTran = tempTran.split(',')
        temp2Tran = temp2Tran.split(',')

        tempTran += temp2Tran   
        transicionesEstado = list(set(tempTran))
        transicionesEstado.sort()

        transicionesEstado = ','.join(transicionesEstado)

        result[letra] = str(transicionesEstado)

        if estado == str(transicionesEstado): 
            resultMatriz[str(transicionesEstado)] = 20

        elif len(estado.split(',')) > len(transicionesEstado.split(',')):
            resultMatriz[str(transicionesEstado)] = 1

        else :
            resultMatriz[str(transicionesEstado)] = 2

    return result, resultMatriz


def dijkstra(Grafo, salida):
    dist, prev = {}, {}
    result = []

    for vertice in Grafo:
        dist[vertice] = float("inf")
        prev[vertice] = None
    dist[salida] = 0

    Q = [vertice for vertice in Grafo]

    while Q:
        u = min(Q, key=dist.get)
        Q.remove(u)
        result.append(u)

        for vecino in Grafo[u]:
            if vecino in Q and dist[vecino] > dist[u] + Grafo[u][vecino]:
                dist[vecino] = dist[u] + Grafo[u][vecino]
                prev[vecino] = u

    return result, dist, prev


def main():
    varTemp = LeerDatosGenrales()

    nroEstados = varTemp[0]
    nroTransiciones = varTemp[1]

    automata, matriz, estadosIniciales = GenerarAutomata(nroEstados)
    estadosIniciales.sort()
    print(matriz)

    AgregarNewEstados(automata, matriz, nroEstados, estadosIniciales)

    # print(matriz)
    # print('\n')

    result2, dist, prev = dijkstra( matriz, '0,1,2,3')

    print('resultado: ', result2)
    print('dist: ' , dist)
    print('prev: ', prev)


# main()




grafo = {
    'a': {'b': 4, 'c': 3},
    'b': {'d': 5},
    'c': {'b': 2, 'd': 3, 'e': 6},
    'd': {'f': 5, 'e': 1},
    'e': {'g': 5},
    'g': {'z': 4},
    'f': {'g': 2, 'z': 7},
    'z': {}
}

grafo2 = {
    '0': {'a': '1', 'b': '1'}, 
    '1': {'a': '1', 'b': '2'}, 
    '2': {'a': '2', 'b': '3'}, 
    '3': {'a': '3', 'b': '0'}, 
    '0,1': {'a': '1', 'b': '1,2'}, 
    '0,2': {'a': '1,2', 'b': '1,3'}, 
    '0,3': {'a': '1,3', 'b': '0,1'}, 
    '1,2': {'a': '1,2', 'b': '2,3'}, 
    '1,3': {'a': '1,3', 'b': '0,2'}, 
    '2,3': {'a': '2,3', 'b': '0,3'}, 
    '0,1,2': {'a': '1,2', 'b': '1,2,3'}, 
    '0,1,3': {'a': '1,3', 'b': '0,1,2'}, 
    '0,2,3': {'a': '1,2,3', 'b': '0,1,3'}, 
    '1,2,3': {'a': '1,2,3', 'b': '0,2,3'}, 
    '0,1,2,3': {'a': '1,2,3', 'b': '0,1,2,3'}
}

grafo3 = {
    '0': {'1': 2, '1': 2}, 
    '1': {'1': 20, '2': 2}, 
    '2': {'2': 20, '3': 2}, 
    '3': {'3': 20, '0': 2}, 
    '0,1': {'1': 1, '1,2': 2}, 
    '0,2': {'1,2': 2, '1,3': 2}, 
    '0,3': {'1,3': 2, '0,1': 2}, 
    '1,2': {'1,2': 20, '2,3': 2}, 
    '1,3': {'1,3': 20, '0,2': 2}, 
    '2,3': {'2,3': 20, '0,3': 2}, 
    '0,1,2': {'1,2': 1, '1,2,3': 2}, 
    '0,1,3': {'1,3': 1, '0,1,2': 2}, 
    '0,2,3': {'1,2,3': 2, '0,1,3': 2}, 
    '1,2,3': {'1,2,3': 20, '0,2,3': 2}, 
    '0,1,2,3': {'1,2,3': 1, '0,1,2,3': 20}
}


# s, distancia, previos = dijkstra(grafo3, '0,1,2,3')
# print(f"{s=}")
# print(f"{distancia=}")
# print(f"{previos=}")



# automata = { '4': {'a': '2', 'b': "3"}, '1': {'a': '3' , 'b': '1'} ,'1,2,3': {'a': '1,2,4', 'b': '1,2'} }

# num = '1,2,3,4'

# num1 = num[(-2+1):]
# num2 = num[:-2]

# result =  HallarTransiciones(automata, num1, num2)
# print("num1: ", result)

# num=[1,2,3,4]
# newNum = [i for i in CrearCombinaciones(num, 2)]
# print(newNum)