import sys
import numpy as np

CHAR_MAP = {
    ".": -1,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "#": 21,
    "$": 22,
    "*": 23,
    "+": 24,
}
NUM_MAP = {v: k for k, v in CHAR_MAP.items()}


def ring_pos(row, col, x_max: int = None, y_max: int = None):
    for x, y in [
        [row - 1, col - 1],
        [row - 1, col],
        [row - 1, col + 1],
        [row, col - 1],
        [row, col + 1],
        [row + 1, col - 1],
        [row + 1, col],
        [row + 1, col + 1],
    ]:
        if (0 <= x < x_max) and (0 <= y < y_max):
            yield (x, y)


def create_mask(positions, array):
    mask = np.zeros_like(array).astype(int)
    for row, col in positions:
        mask[row, col] = 1
    return mask


def digit_mask(array):
    mask = np.zeros_like(array).astype(int)
    digit_positions = np.where(np.vectorize(lambda x: NUM_MAP[x].isdigit())(array))
    for row, col in zip(*digit_positions):
        mask[row, col] = 1
    return mask


if __name__ == "__main__":
    array = []
    with open(sys.argv[1], "r") as f:
        for line in f:
            array.append([CHAR_MAP[i] for i in line.strip()])
    array = np.array(array)
    print(array)
    print(digit_mask(array))

    symbols = [
        i for i in np.unique(array) if not (NUM_MAP[i].isdigit() or (NUM_MAP[i] == "."))
    ]
    print(symbols)

    symbol_positions = np.where(np.isin(array, symbols))
    for row, col in zip(*symbol_positions):
        ring = []
        for rp in ring_pos(row, col, array.shape[0], array.shape[1]):
            ring.append(rp)
        ring = np.array(ring)
        print(f"{row}x{col}: ->")
        print(create_mask(ring, array))
