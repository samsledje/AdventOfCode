import sys
import numpy as np
from scipy.signal import convolve2d

CONV_FILTER = np.ones((3, 3))
CONV_FILTER[1, 1] = 0

THRESH = 4

if __name__ == "__main__":
    floor_map = []
    total_removed = 0

    with open(sys.argv[1], "r") as f:
        for line in f:
            floor_map.append([1 if i == "@" else 0 for i in line.strip()])
    floor_map = np.array(floor_map)
    print(floor_map)

    num_available = floor_map.shape[0]
    while num_available:
        num_adjacent = convolve2d(floor_map, CONV_FILTER, boundary="fill")[1:-1, 1:-1]

        is_available = (num_adjacent < THRESH).astype(int) * floor_map
        num_available = np.sum(is_available)
        total_removed += num_available
        floor_map = floor_map - is_available
        print(floor_map)
        print("#" * 30)

    print(total_removed)
