import sys
import numpy as np
from scipy.signal import convolve2d

CONV_FILTER = np.ones((3, 3))
CONV_FILTER[1, 1] = 0

THRESH = 4

if __name__ == "__main__":
    floor_map = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            floor_map.append([1 if i == "@" else 0 for i in line.strip()])
    floor_map = np.array(floor_map)

    print("Base map:")
    print(floor_map)
    print("#" * 20)

    num_adjacent = convolve2d(floor_map, CONV_FILTER, boundary="fill")[1:-1, 1:-1]

    print("Adjacency count:")
    print(num_adjacent)
    print("#" * 20)

    is_available = (num_adjacent < THRESH).astype(int) * floor_map

    print(is_available)
    print("#" * 20)

    rolls_available = np.sum(is_available)
    print(rolls_available)
