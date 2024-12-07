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

FW_CHECK = np.array([1, 2, 3, 4])
RV_CHECK = np.array([4, 3, 2, 1])

MAIN_DIAG_MASK = np.eye(4)
REV_DIAG_MASK = np.fliplr(np.eye(4))
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

    # map 1 & 2
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if np.array_equal(arr[i, j:j+4], FW_CHECK):
                hits.append((i, j, arr[i, j:j+4], "FW"))
            if np.array_equal(arr[i, j:j+4], RV_CHECK):
                hits.append((i, j, arr[i, j:j+4], "RV"))
    
    # map 1 & 2 (transposed)
    for j in range(arr.shape[1]):
        for i in range(arr.shape[0]):
            if np.array_equal(arr[i:i+4, j], FW_CHECK):
                hits.append((i, j, arr[i:i+4, j], "DOWN"))
            if np.array_equal(arr[i:i+4, j], RV_CHECK):
                hits.append((i, j, arr[i:i+4, j], "UP"))

    # map 3 & 4
    for i in range(arr.shape[0] - 3):
        for j in range(arr.shape[1] - 3):
            sqr = arr[i:i+4, j:j+4]
            fw_diag = np.diagonal(sqr * MAIN_DIAG_MASK).astype(int)
            rv_diag = np.diagonal(np.fliplr(sqr * REV_DIAG_MASK)).astype(int)

            if np.array_equal(fw_diag, FW_CHECK.squeeze()):
                hits.append((i, j, fw_diag, "FW_MAIN"))
            if np.array_equal(fw_diag, RV_CHECK.squeeze()):
                hits.append((i, j, fw_diag, "RV_MAIN"))
            if np.array_equal(rv_diag, FW_CHECK.squeeze()):
                hits.append((i, j, rv_diag, "FW_REV"))
            if np.array_equal(rv_diag, RV_CHECK.squeeze()):
                hits.append((i, j, rv_diag, "RV_REV"))

    for h in hits:
        print(h)
    print(len(hits))
