import sys
import numpy as np

def letter_map(c):
    D = {
        "X": 1,
        "M": 2,
        "A": 3,
        "S": 4,
    }
    if c in D:
        return D[c]
    return 0

CORRECT_CHECKS = [
    np.array([
    [2, 0, 2],
    [0, 3, 0],
    [4, 0, 4]]),
    np.array([
    [2, 0, 4],
    [0, 3, 0],
    [2, 0, 4]]),
    np.array([
    [4, 0, 2],
    [0, 3, 0],
    [4, 0, 2]]),
    np.array([
    [4, 0, 4],
    [0, 3, 0],
    [2, 0, 2]])
]

MASK = np.array([
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
])
# maps = [np.array(m) for m in [MAP1, MAP2, MAP3, MAP4]]

if __name__ == "__main__":
    file = sys.argv[1]

    arr = []
    with open(file, "r") as f:
        for line in f:
            arr.append(np.array([letter_map(c) for c in line.strip()]))
    arr = np.array(arr)
    print(arr)

    count = 0
    hits = []

    # map 3 & 4
    for i in range(arr.shape[0] - 2):
        for j in range(arr.shape[1] - 2):
            sqr = arr[i:i+3, j:j+3]
            sqrmask = sqr * MASK

            # if np.array_equal(sqrmask, CORRECT_CHECK):
            #     hits.append((i, j, sqrmask, "MAIN"))
            # if np.array_equal(sqrmask, np.fliplr(CORRECT_CHECK)):
            #     hits.append((i, j, sqrmask, "MAINLR"))
            # if np.array_equal(sqrmask, np.flipud(CORRECT_CHECK)):
            #     hits.append((i, j, sqrmask, "MAINUD"))
            # if np.array_equal(sqrmask, CORRECT_CHECK_2):
            #     hits.append((i, j, sqrmask, "MAIN2"))
            # if np.array_equal(sqrmask, np.fliplr(CORRECT_CHECK)):
            #     hits.append((i, j, sqrmask, "MAIN2LR"))
            # if np.array_equal(sqrmask, np.flipud(CORRECT_CHECK_2)):
            #     hits.append((i, j, sqrmask, "MAIN2UD"))

            for m in CORRECT_CHECKS:
                if np.array_equal(sqrmask, m):
                    hits.append((i, j))

    for h in set(hits):
        print(h)
    print(len(set(hits)))
