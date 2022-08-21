#!/usr/bin/python3

import sys


def read_automaton(filename):
    # Read all integers in filename 
    numbers = []
    with open(filename, 'r') as f:
        numbers = [int(x) for x in f.read().split()]

    # Extract n (number of states) and k (size of the alphabet)
    n = numbers[0]
    k = numbers[1]

    # Check that the transition matrix was encoded in filename
    if len(numbers) != 2 + k * n:
        sys.stderr.write('Warning: automaton in text file ' + filename + ' was encoded incorrectly.\n')
    if len(numbers) < 2 + k * n:
        sys.exit(1)

    # Construct transition matrix from the numbers in the file
    D = []
    for i in range(n):
        D.append([numbers[m] for m in range(2 + k * i, 2 + k * (i + 1))])

    # Return the DFA
    return (n, k, D)

# Read input word and convert its charaters into integers in range(k) 
def read_word():
    return [ord(c) - ord('a') for c in sys.stdin.read().split()[0]]

# From each state in the DFA, see which state the word w yields 
def simulate(n, k, D, w):
    states = list(range(n))
    for i in range(n):
        for j in range(len(w)):
            states[i] = D[states[i]][w[j]]

    return states

def main():
    # Show a little help
    if len(sys.argv) < 2:
        print("Modo de usar:\n\n\tcheck.py arquivo_automato\n" +
              "\nLee el DFA M del arquivo_automato y lee una palabra w de la " +
              "entrada estandar.\n Devuelve 0 si la palabra sincroniza y 1 " +
              "caso contrário.")
        sys.exit(1)

    # Read everything into memory
    n, k, D = read_automaton(sys.argv[1])

    if len(sys.argv) > 2:
        w = [ord(c) - ord('a') for c in sys.argv[2].split()[0]]
    else:
        w = read_word()

    # Verifica que os símbolos da palavra estão entre 'a' e 'z'
    for c in w:
        if c < 0 or c > ord('z') - ord('a'):
            sys.exit(1)

    # Simulate
    states = simulate(n, k, D, w)

    # Check that synchronization has occurred
    if len(set(states)) > 1:
        sys.stderr.write('No sincroniza! Estados restantes: ')
        restantes = list(set(states))
        for estado in restantes:
            sys.stderr.write(str(estado) + ' ')
        # print(set(states))
        # print('NAO')
        sys.exit(1)
    else:
        sys.stderr.write('Sincroniza para el estado ' + str(states[0]) + '\n')
        # print('SIM')
        sys.exit(0)

if __name__ == "__main__":
    main()


