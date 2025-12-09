import sys
import numpy as np
from shapely import Polygon
from tqdm import tqdm


def reorder(a, b):
    if a < b:
        return a, b
    else:
        return b, a


def compute_rectangle_size(x1: int, y1: int, x2: int, y2: int):
    return (np.abs(x2 - x1) + 1) * (np.abs(y2 - y1) + 1)


def fill_green(x1: int, y1: int, x2: int, y2: int):
    if x1 == x2:
        y1, y2 = reorder(y1, y2)
        return np.array([[x1, y] for y in range(y1 + 1, y2)])
    elif y1 == y2:
        x1, x2 = reorder(x1, x2)
        return np.array([[x, y1] for x in range(x1 + 1, x2)])
    else:
        raise ValueError("Either row or column must be the same.")


if __name__ == "__main__":
    last_x, last_y = None, None
    reds = []
    greens = []

    with open(sys.argv[1], "r") as f:
        # tile_positions = np.array(
        #     [[int(num) for num in line.strip().split(",")] for line in f]
        # )

        for line in f:
            x, y = line.strip().split(",")
            x, y = int(x), int(y)
            reds.append([x, y])
            if last_x is None:
                first_x, first_y = x, y
            else:
                greens.append(fill_green(x, y, last_x, last_y))
            last_x, last_y = x, y
    greens.append(fill_green(last_x, last_y, first_x, first_y))

    reds = np.array(reds)
    greens = np.concatenate(greens)

    grid_size = np.max(reds[0]) + 1, np.max(reds[1]) + 1
    grid = np.zeros(grid_size)

    for rx, ry in reds:
        grid[ry, rx] = 1
    for gx, gy in greens:
        grid[gy, gx] = 2

    pgon = Polygon(reds).buffer(1e-4)
    max_size = 0
    max_coords = None

    print(grid)
    print("###########")

    print(reds)

    # turns out you can brute force this with a sufficiently fast contains algorithm
    # 15 seconds isn't "fast" but it's fast enough for me
    for x1, y1 in tqdm(reds):
        for x2, y2 in reds:
            # print(x1, y1, x2, y2)
            # x1, x2 = reorder(x1, x2)
            # y1, y2 = reorder(y1, y2)
            rect = Polygon([(x1, y1), (x1, y2), (x2, y1), (x2, y2)])
            # gcopy = grid.copy()
            # gcopy[y1, x1] = 9
            # gcopy[y2, x1] = 9
            # gcopy[y1, x2] = 9
            # gcopy[y2, x2] = 9
            # print(gcopy)
            rect_size = rect_size = compute_rectangle_size(x1, y1, x2, y2)
            # print(rect_size)
            if pgon.contains(rect):
                if rect_size > max_size:
                    max_size = rect_size
                    max_coords = [x1, y1, x2, y2]
    print(max_size)
