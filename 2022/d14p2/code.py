import sys
import numpy as np

all_rocks = []

maxx = 0
maxy = 0
with open(sys.argv[1],'r') as f:
    for line in f:
        coords = []
        for p in line.strip().split(' -> '):
            i,j = p.split(',')
            maxy = max(maxy,int(j))
            maxx = max(maxx,int(i))
            coords.append(np.array([int(j), int(i)]))
        all_rocks.append(coords)

cave = np.zeros((maxy+3,10000))
cave[-1,:] = 2
print(cave.shape)


for rock in all_rocks:
    for i in range(len(rock)-1):
        strt = rock[i]
        end = rock[i+1]
        strt_i, strt_j = strt[0],strt[1]
        end_i, end_j = end[0],end[1]
        if strt_i == end_i:
            low = min(strt_j, end_j)
            hi = max(strt_j, end_j)
            cave[strt_i, low:hi+1] = 2
        elif strt_j == end_j:
            low = min(strt_i, end_i)
            hi = max(strt_i, end_i)
            cave[low:hi+1,strt_j] = 2

charmap = {
        0: '.',
        1: 'o',
        2: '#',
        }

def pprint_cave(cave):
    for i in range(cave.shape[0]):
        for j in range(cave.shape[1]):
            print(charmap[cave[i,j]],end='')
        print('')

def sand_fall(cave,i,j):
    if cave[i+1,j] < cave[i,j]:
        cave[i+1,j] = 1
        cave[i,j] = 0
        return (cave, i+1, j, False)
    elif cave[i+1,j-1] < cave[i,j]:
        cave[i+1,j-1] = 1
        cave[i,j] = 0
        return (cave, i+1, j-1, False)
    elif cave[i+1,j+1] < cave[i,j]:
        cave[i+1,j+1] = 1
        cave[i,j] = 0
        return (cave, i+1, j+1, False)
    else:
        return (cave, i, j, True)

import time

settled = False
i,j = 0,500
n_grains = 0
while i >= 0:
    n_grains += 1
    i,j = 0,500
    cave[i,j] = 1
    settled = False
    while not settled:
        #print('=================')
        #pprint_cave(cave[:20,485:515])
        (cave,i,j,settled) = sand_fall(cave,i,j)

    if (i == 0) and (j == 500):
        break

pprint_cave(cave[:,485:515])
print(n_grains)
