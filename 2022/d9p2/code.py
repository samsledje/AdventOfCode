import sys
import numpy as np

START_POS = np.array([0,0])
ROPE_LEN = 10
tail_rec = set([tuple(START_POS)])

head_pos = START_POS
tail_pos = START_POS

rope_pos = []
for _ in range(ROPE_LEN):
    rope_pos.append(START_POS)
rope_pos = np.array(rope_pos)

def draw_grid(head_pos, tail_pos):
    hx, hy = head_pos
    tx, ty = tail_pos

    for j in range(4, -1, -1):
        for i in range(6):
            if (i,j) == (hx, hy):
                print('H', end='')
            elif (i,j) == (tx, ty):
                print('T', end='')
            else:
                print('.', end='')
        print('')

def update_head(head_pos, direction):
    if direction == 'L':
        head_pos_update = head_pos + np.array([-1, 0])
    elif direction == 'R':
        head_pos_update = head_pos + np.array([1, 0])
    elif direction == 'U':
        head_pos_update = head_pos + np.array([0, 1])
    elif direction == 'D':
        head_pos_update = head_pos + np.array([0, -1])
    return head_pos_update

def update_tail(head_pos, tail_pos):
    hx, hy = head_pos
    tx, ty = tail_pos

    if (np.abs(hx - tx) > 1) or (np.abs(hy - ty) > 1):
        tail_pos_update = np.array([tx - np.sign(tx - hx), ty - np.sign(ty - hy)])
    else:
        tail_pos_update = np.array([tx, ty])
    return tail_pos_update

def update(head_pos, tail_pos, direction):
    head_pos_update = update_head(head_pos, direction)
    tail_pos_update = update_tail(head_pos_update, tail_pos)
    return (head_pos_update, tail_pos_update)

def update_rope(rope_pos, direction):
    rope_pos[0, :] = update_head(rope_pos[0,:], direction)
    for i in range(1, ROPE_LEN):
        rope_pos[i, :] = update_tail(rope_pos[i-1, :], rope_pos[i, :])
    return (rope_pos)

step_list = []
with open(sys.argv[1],'r') as f:
    for line in f:
        direction, n_steps = line.strip().split()
        step_list.append((direction, int(n_steps)))

draw_grid(head_pos, tail_pos)
for (d, n) in step_list:
    for _ in range(n):
        rope_pos = update_rope(rope_pos, d)
        tail_rec.add(tuple(rope_pos[-1, :]))

print(len(tail_rec))
