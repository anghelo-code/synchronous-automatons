#!/usr/bin/python3

import sys


if len(sys.argv) < 2:
    sys.stderr.write('Modo de usar:\n\n\t\tdifficult n' + 
                     '\n\n\t\twhere n is the number of states.')
    sys.exit(1)
    
n = int(sys.argv[1])

print(n, 2)

print('1 1')
for i in range(1, n - 1):
    print(i, i + 1)
print(n - 1, 0)


    
