import sys
import numpy as np

START_POS = np.array([0, 0])
tail_rec = set([tuple(START_POS)])

head_pos = START_POS
tail_pos = START_POS

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

step_list = []
with open(sys.argv[1],'r') as f:
    for line in f:
        direction, n_steps = line.strip().split()
        step_list.append((direction, int(n_steps)))

draw_grid(head_pos, tail_pos)
for (d, n) in step_list:
    for _ in range(n):
        (head_pos, tail_pos) = update(head_pos, tail_pos, d)
#        print(d, head_pos, tail_pos)
#        draw_grid(head_pos, tail_pos)
        tail_rec.add(tuple(tail_pos))

print(len(tail_rec))
