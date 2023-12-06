import sys
import numpy as np
from scipy.sparse.csgraph import shortest_path
from tqdm import tqdm

landscape = []

with open(sys.argv[1],'r') as f:
    row = []
    for i, line in enumerate(f):
        for j, c in enumerate(line.strip()):
            if c == 'S':
                nc = 0
                start_pos = (i,j)
            elif c == 'E':
                nc = 26
                end_pos = (i,j)
            else:
                nc = ord(c) - 97
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
print(start_pos, end_pos)
start_ind = start_pos[0] * map_shape[1] + start_pos[1]
end_ind = end_pos[0] * map_shape[1] + end_pos[1]
print(start_ind, end_ind)

path_length = dist_matrix[start_ind, end_ind]
print(path_length)
