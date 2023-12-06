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

cave = np.zeros((maxy+2,maxx+10))
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

with np.printoptions(threshold=np.inf):
    #print(cave[:10,493:505])
    #print(cave[149:152,450:465])
    #print(cave[:150,495:505])
    pass

def sand_fall(cave,i,j):
    try:
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
    except IndexError:
        return (cave, None, None, True)

settled = False
i,j = 0,500
n_grains = 0
while i is not None:
    n_grains += 1
    i,j = 0,500
    cave[i,j] = 1
    settled = False
    while not settled:
        (cave,i,j,settled) = sand_fall(cave,i,j)
        print('======')
        print(cave[:10,490:505])

print(n_grains-1)
