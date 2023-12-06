import sys
import re

def move(D, src, dest, n):
    for _ in range(n):
        x = D[src-1].pop()
        D[dest-1].append(x)

    return D

stacks = {}

with open(sys.argv[1],'r') as f:
    for line in f:
        if line.strip().startswith('1'):
            n_stacks = max([int(i) for i in line.split()])
            print(n_stacks)

for n in range(n_stacks):
    stacks[n] = []

with open(sys.argv[1],'r') as f:
    for line in f:
        if line.lstrip()[0] == '1':
            break
        for s, c in zip(stacks.keys(), line[1::4]):
            if c != ' ':
                stacks[s].append(c)

for _,v in stacks.items():
    v.reverse()

re_string = 'move (\d+) from (\d+) to (\d+)'

with open(sys.argv[1],'r') as f:
    for line in f:
        if not line.startswith('move'):
            continue
        m = re.search(re_string, line.strip())
        n = int(m[1])
        src = int(m[2])
        dest = int(m[3])
        stacks = move(stacks,src,dest,n)

readout = []
for v in stacks.values():
    readout.append(v[-1])
print(''.join(readout))
