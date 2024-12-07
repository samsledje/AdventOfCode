import sys
import time
import numpy as np

CHAR_TO_INT = {
    ".": -1,
    "#": -2,
    "^": 0,
    ">": 1,
    "v": 2,
    "<": 3,
}

INT_TO_CHAR = {
    -1: ".",
    -2: "#",
    0: "^",
    1: ">",
    2: "v",
    3: "<",
}

def viz_map(arr):
    for row in arr:
        for val in row:
            print(INT_TO_CHAR[val], end="")
        print()

def init_map(data):

    arr = []
    for line in data.split("\n"):
        linearr = []
        for char in line.strip():
            linearr.append(CHAR_TO_INT[char])
            if CHAR_TO_INT[char] in [0,1,2,3]:
                init_pos = (len(arr), len(linearr)-1)
                init_dir = CHAR_TO_INT[char]
        arr.append(linearr)

    return np.array(arr), init_pos, init_dir

def guard_forward(guard_pos, guard_dir):
    x,y = guard_pos
    if guard_dir == 0:
        return (x-1, y)
    elif guard_dir == 1:
        return (x, y+1)
    elif guard_dir == 2:
        return (x+1, y)
    elif guard_dir == 3:
        return (x, y-1)

def guard_step(arr, guard_pos, guard_dir):

    guard_fw = guard_forward(guard_pos, guard_dir)
    if arr[guard_fw] == -1: # empty space
        arr[guard_pos] = -1
        arr[guard_fw] = guard_dir
        return arr, guard_fw, guard_dir
    elif arr[guard_fw] == -2: # wall
        guard_dir = (guard_dir + 1) % 4 #rotate guard
        arr[guard_pos] = guard_dir
        return arr, guard_pos, guard_dir

if __name__ == "__main__":

    with open(sys.argv[1]) as f:
        data = f.read()

    arr, gp, gd = init_map(data)
    VISITED = np.zeros_like(arr)

    # viz_map(arr)
    # print("#################")
    
    while True:
        try:
            arr, gp, gd = guard_step(arr, gp, gd)
            VISITED[gp] = 1
            # viz_map(arr)
            # print("#################")
        except IndexError:
            print("Guard out of bounds")
            break
    # viz_map(arr)
    # print(VISITED)
    print(np.sum(VISITED))