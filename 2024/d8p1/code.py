import sys
import numpy as np
from itertools import combinations

def ord_null(c):
    if c == "#":
        return -1
    elif c == ".":
        return 0
    return ord(c)

def chr_null(c):
    if c == -1:
        return "#"
    elif c == 0:
        return "."
    return chr(c)

def build_map(fi):
    arr = []
    for l in fi:
        arr.append([ord_null(a) for a in l.strip()])
    return np.array(arr)

def viz_map(arr):
    print("  ", end="")
    print(" ".join([str(i)[-1] for i in np.arange(arr.shape[1])]))
    for i, l in enumerate(arr):
        print(str(i)[-1], end=" ")
        print(" ".join([chr_null(a) for a in l]))

def check_antinode_bounds(x, y, arr):
    if x < 0 or x >= arr.shape[1]:
        return False
    if y < 0 or y >= arr.shape[0]:
        return False
    return True

def find_antinodes(posOne, posTwo, arr):

    if posOne[1] <= posTwo[1]:
        posA = posOne
        posB = posTwo
    else:
        posA = posTwo
        posB = posOne
    ay, ax = posA
    by, bx = posB

    slope = (by - ay) / (bx - ax)
    xdist = abs(ax - bx)
    ydist = abs(ay - by)
    # dist = abs(ax - bx) + abs(ay - by)

    if (slope > 0):
        anodes = [(ay - ydist, ax - xdist), (by + ydist, bx + xdist)]
    elif (slope < 0):
        anodes = [(ay + ydist, ax - xdist), (by - ydist, bx + xdist)]
    anodes_valid = [x for x in anodes if check_antinode_bounds(x[0], x[1], arr)]
    return anodes_valid

def update_antinode_map(arr, y, x):
    arr[y, x] = -1
    return arr

def find_nodes(arr):
    unique_values = np.unique(arr)
    unique_values = [i for i in unique_values if i != 0]

    node_locations = {}
    for tower_type in unique_values:
        tower_coords = np.where(arr == tower_type)
        tower_coords = list(zip(tower_coords[0], tower_coords[1]))
        node_locations[tower_type] = tower_coords

    return node_locations

if __name__ == "__main__":
    
    with open(sys.argv[1], "r") as f:
        arr = build_map(f)

    # print(arr)
    # viz_map(arr)

    # print(find_antinodes((2, 5), (4, 4), arr))
    node_locations = find_nodes(arr)

    # antinodes_verbose = set()
    antinode_locations = set()
    for k,v in node_locations.items():
        for i, j in combinations(v, 2):
            # anodes = find_antinodes(i, j, arr)
            # for an in anodes:
            #     antinodes_verbose.add((i,j,an))
            antinode_locations.update(find_antinodes(i, j, arr))

    # print(antinodes_verbose)
    for anl in antinode_locations:
        arr = update_antinode_map(arr, anl[0], anl[1])
    viz_map(arr)

    print(len(antinode_locations))


    