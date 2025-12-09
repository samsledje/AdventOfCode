import sys
import numpy as np


def compute_rectangle_size(x1: int, y1: int, x2: int, y2: int):
    return (np.abs(x2 - x1) + 1) * (np.abs(y2 - y1) + 1)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        tile_positions = np.array(
            [[int(num) for num in line.strip().split(",")] for line in f]
        )
    grid_size = np.max(tile_positions[0]) + 1, np.max(tile_positions[1]) + 1
    grid = np.zeros(grid_size)

    max_area = 0
    # We're going to try lazy brute force first
    for x1, y1 in tile_positions:
        for x2, y2 in tile_positions:
            rsize = compute_rectangle_size(x1, y1, x2, y2)
            if rsize > max_area:
                max_area = rsize
    print(max_area)
    # Yeah turns out you can brute force this though I don't feel good about it
