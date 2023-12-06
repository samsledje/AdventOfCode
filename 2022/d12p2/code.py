import sys
import numpy as np
from scipy.sparse.csgraph import shortest_path
from tqdm import tqdm

landscape = []

start_pos = []
with open(sys.argv[1],'r') as f:
    row = []
    for i, line in enumerate(f):
        for j, c in enumerate(line.strip()):
            if c == 'S':
                nc = 0
                start_pos.append((i,j))
            elif c == 'E':
                nc = 26
                end_pos = (i,j)
            else:
                nc = ord(c) - 97
                if nc == 0:
                    start_pos.append((i,j))
            row.append(nc)
        landscape.append(row)
        row = []
    landscape = np.array(landscape)

map_shape = landscape.shape

print(landscape)

def manhattan(x, y):
    return np.sum(np.abs(np.array(x) - np.array(y)))

height_difference = np.subtract.outer(landscape.ravel(), landscape.ravel())
height_allowed = (height_difference >= -1).astype(int)

iter1 = np.nditer(landscape, flags=['multi_index'])

travel_allowed = []
for _ in tqdm(iter1,total=map_shape[0]*map_shape[1]):
    iter2 = np.nditer(landscape, flags=['multi_index'])
    for _ in iter2:
        travel_allowed.append(manhattan(iter1.multi_index,iter2.multi_index))
travel_distance = np.array(travel_allowed).reshape(height_allowed.shape)
travel_allowed = (travel_distance <= 1).astype(int)

travel_graph = height_allowed * travel_allowed
print(travel_graph)

dist_matrix = shortest_path(travel_graph)

print(map_shape)

def get_index(pos, map_shape):
    return pos[0] * map_shape[1] + pos[1]

end_ind = get_index(end_pos, map_shape)

possible_paths = []
for sp in start_pos:
    start_ind = get_index(sp, map_shape)
    path_length = dist_matrix[start_ind, end_ind]
    possible_paths.append(path_length)

print(min(possible_paths))
