#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random as rd
import sys

# Generates the transition matrix of a random n-state DFA on k symbols
def generate(n, k):
    return (n, k, [[rd.randint(0, n - 1) for i in range(k)] for j in range(n)])

# Take the n-state DFA on k symbols M and multiply each state by a factor of at most r
def lift(n, k, M, r):
    # Determine how many states correspond to each of the original states 
    L = [rd.randint(1, r) for i in range(n)]

    # S[i] = L[i - 1] + ... + L[0]
    S = [0] + list(L);
    for i in range(1, n + 1):
        S[i] += S[i - 1]

    # Create new transition matrix T
    T = []
    for i in range(n):
        for l in range(L[i]):
            T.append([S[M[i][j]] + rd.randint(0, L[M[i][j]] - 1) for j in range(k)])         
    return (S[n], k, T)

# Shuffle the states of a DFA 
def shuffle(n, k, M):
    # Create random permutation 
    p = list(range(n))
    rd.shuffle(p)

    # Compute its inverse
    q = list(range(n))
    for i in range(n):
        q[p[i]] = i

    # Create new transition matrix T    
    T = []
    for i in range(n):
        T.append([q[s] for s in M[p[i]]])

    return (n, k, T)

# Generate a text encoding of the DFA 
def automaton2string(n, k, M):
    s = str(n) + ' ' + str(k) + '\n'
    for i in range(n):
        for j in range(k):
            s += str(M[i][j]) + ' '
        s += '\n'
    return s

# Creates a text file with content s
def save(s):
    save.counter += 1
    with open('file' + str(save.counter), 'w') as f:
        f.write(s)

save.counter = 0

def main():
    numbers = [int(x) for x in sys.stdin.read().split()]
    numbers.append(None)
    for n, k, r in zip(numbers[::3], numbers[1::3],  numbers[2::3]):
        save(automaton2string(*shuffle(*lift(*generate(n, k), r))))

def test(N):
    for i in range(N):
        n, k, r = rd.randint(4, 200), rd.randint(1, 26), rd.randint(1, 10)
        n, k, M = lift(*generate(n, k), r)
        if n <= 1000:
            save(automaton2string(*shuffle(n, k, M)))

if __name__ == "__main__":
    test(200)
