import sys
import numpy as np
import time
from tqdm import tqdm

CHAR_TO_INT = {
    ".": -1,
    "#": -2,
    "^": 0,
    ">": 1,
    "v": 2,
    "<": 3,
    "O": -3,
}

INT_TO_CHAR = {
    -1: ".",
    -2: "#",
    -3: "O",
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
    if guard_fw[0] < 0 or guard_fw[1] < 0 or guard_fw[0] >= arr.shape[0] or guard_fw[1] >= arr.shape[1]:
        raise IndexError
    if arr[guard_fw] == -1: # empty space
        arr[guard_pos] = -1
        arr[guard_fw] = guard_dir
        return arr, guard_fw, guard_dir
    elif arr[guard_fw] <= -2: # wall
        guard_dir = (guard_dir + 1) % 4 #rotate guard
        arr[guard_pos] = guard_dir
        return arr, guard_pos, guard_dir

def place_obstacle(arr, pos):
    x,y = pos
    new_arr = arr.copy()
    new_arr[x,y] = -3
    return new_arr

if __name__ == "__main__":

    with open(sys.argv[1]) as f:
        data = f.read()

    orig_arr, init_gp, init_gd = init_map(data)
    viz_map(orig_arr)
    print("#################")
    VISITED = np.zeros_like(orig_arr)

    # test initial path
    arr = orig_arr.copy()
    gp = init_gp
    gd = init_gd
    print(init_gd, init_gp)
    while True:
        try:
            arr, gp, gd = guard_step(arr, gp, gd)
            VISITED[gp] = 1
            # viz_map(arr)
            # print("#################")
        except IndexError:
            print("Guard out of bounds")
            break
    
    # extract all positions visited on the original path
    possible_spots = np.argwhere((VISITED == 1) & (orig_arr == -1))
    loop_spots = []

    for p in tqdm(possible_spots):
        arr = place_obstacle(orig_arr, p)
        gp = init_gp
        gd = init_gd
        VISITED_POS = set()

        n_steps = 0
        while True:
            n_steps += 1
            try:
                arr, gp, gd = guard_step(arr, gp, gd)
                # viz_map(arr)
                # print("#################")
                # time.sleep(0.1)
                if (gp[0], gp[1], gd) in VISITED_POS:
                    loop_spots.append((p[0], p[1]))
                    # print(f"Loop found at {p[0], p[1]} after {n_steps} steps")
                    break

                VISITED_POS.add((gp[0], gp[1], gd))
            except IndexError:
                # print(f"Guard out of bounds after {n_steps} steps")
                # time.sleep(0.5)
                break
        
    print(sorted(list(set(loop_spots))))
    print(len(set(loop_spots)))