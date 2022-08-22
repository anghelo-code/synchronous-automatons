
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
    listaEstados = []
    for i in range(nroEstados):
        transiciones = LeerTransiciones()
        AgregarAListaEstados(listaEstados, transiciones)

        CrearEstado(transiciones, automata, i)

    if len(listaEstados) < nroEstados:
        return False         

    return [automata, listaEstados]

def CrearEstado(transiciones, automata, estado):
    estadoCreado = CrearTransiciones(transiciones)
    automata[str(estado)] = estadoCreado
    return automata


def AgregarAListaEstados(arreglo, transiciones):
    for i in transiciones:
        if i not in arreglo:
            arreglo.append(i)


def CrearTransiciones(transicionesEstado):
    result = {}
    abecedario = "abcdefghijklmnopqrstuvwxyz"

    for i in range(len(transicionesEstado)):
        letra = abecedario[i]
        result[letra] = str(transicionesEstado[i])
    return result



def ResolverProblema(automata):
    print()
    return ""


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


def AgregarNewEstados(automata, nroEstados, estadosIniciales):
    estados =  []

    for i in range(2,nroEstados+1):
        estados.extend(CrearCombinaciones(estadosIniciales, i))

    AgregarValores(estados, automata)


def AgregarValores(estados, automata):
    for estado in estados:
        i=-1
        estado = ','.join(estado)
        while estado[i] != ",":
            i-=1
    
        estadoUnico = estado[(i+1):]
        oldEstado = estado[:i]

        transiciones = HallarTransiciones(automata, estadoUnico, oldEstado)

        automata[estado] = transiciones


def HallarTransiciones(automata, estadoUnico, oldEstado):
    result = {}
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

    return result


def main():
    varTemp = LeerDatosGenrales()

    nroEstados = varTemp[0]
    nroTransiciones = varTemp[1]

    result = GenerarAutomata(nroEstados)
    automata = result[0]
    estadosIniciales = result[1]
    estadosIniciales.sort()

    AgregarNewEstados(automata, nroEstados, estadosIniciales)

    # resultado = ResolverProblema(automata)
    # print(resultado)

    print(automata)


main()

# automata = { '4': {'a': '2', 'b': "3"}, '1': {'a': '3' , 'b': '1'} ,'1,2,3': {'a': '1,2,4', 'b': '1,2'} }

# num = '1,2,3,4'

# num1 = num[(-2+1):]
# num2 = num[:-2]

# result =  HallarTransiciones(automata, num1, num2)
# print("num1: ", result)

# num=[1,2,3,4]
# newNum = [i for i in CrearCombinaciones(num, 2)]
# print(newNum)