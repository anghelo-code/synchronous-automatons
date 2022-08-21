transiciones = "abcdefghijklmnopqrstuvwxyz"

def LeerDatosGenrales():
    nroEstados = int(input())
    nroTransiciones = int(input())
    return [nroEstados, nroTransiciones]


def LeerTransiciones():
    transiciones = input().split()
    return transiciones


def GenerarAutomata(nroEstados):
    automata = []
    listaEstados = []
    for i in range(nroEstados):
        transiciones = LeerTransiciones()
        AgregarAListaEstados(listaEstados, transiciones)

        CrearEstado(transiciones, automata)

    if len(listaEstados) < nroEstados:
        return False         

    return automata

def CrearEstado(transiciones, automata):
    estado = CrearTransiciones(transiciones)
    automata.append(estado)
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
        result[letra] = int(transicionesEstado[i])
    return result


def GenerarTransiciones(transicionesEstado):
    result = {}
    abecedario = "abcdefghijklmnopqrstuvwxyz"

    for i in range(len(transicionesEstado)):
        letra = abecedario[i]
        result[letra] = int(transicionesEstado[i])
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

    



def main():
    varTemp = LeerDatosGenrales()

    nroEstados = varTemp[0]
    nroTransiciones = varTemp[1]

    automata = GenerarAutomata(nroEstados)

    # resultado = ResolverProblema(automata)
    # print(resultado)

    print(automata)


# main()

num=[1,2,3,4]
newNum = [i for i in CrearCombinaciones(num, 2)]
print(newNum)