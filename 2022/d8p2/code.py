import sys
import numpy as np

FM = []

with open(sys.argv[1],'r') as f:
    for line in f:
        FM.append(np.array([int(i) for i in line.strip()]))
FM = np.array(FM)

def is_visible(FM, ind_i, ind_j, DEBUG=False):
    height = FM[ind_i, ind_j]

    viz_left = (FM[ind_i,:ind_j] < height).all()
    viz_right = (FM[ind_i,(ind_j+1):] < height).all()
    viz_above = (FM[:ind_i,ind_j] < height).all()
    viz_below = (FM[(ind_i+1):,ind_j] < height).all()

    if DEBUG:
        print('===')
        print(viz_left, FM[ind_i, :ind_j])
        print(viz_right, FM[ind_i, (ind_j+1):])
        print(viz_above, FM[:ind_i, ind_j])
        print(viz_below, FM[(ind_i+1):,ind_j])
    return (viz_left or viz_right or viz_above or viz_below)

def score_view(view, height, direction=True):
    score = 0
    if not direction:
        view = view[::-1]
    for t in view:
        score += 1
        if t >= height:
            return score
    return score

def scenic_score(FM, ind_i, ind_j, DEBUG=False):
    height = FM[ind_i, ind_j]

    left_view = FM[ind_i, :ind_j]
    left_score = score_view(left_view, height, False)
    right_view = FM[ind_i, (ind_j+1):]
    right_score = score_view(right_view, height)
    above_view = FM[:ind_i, ind_j]
    above_score = score_view(above_view, height, False)
    below_view = FM[(ind_i+1):, ind_j]
    below_score = score_view(below_view, height)

    if DEBUG:
        print(ind_i, ind_j, FM[ind_i, ind_j])
        print(left_view, left_score)
        print(right_view, right_score)
        print(above_view, above_score)
        print(below_view, below_score)
        print("===")

    return np.product([left_score, right_score, above_score, below_score])

max_scenic = 0
print(FM)
for i in range(FM.shape[0]):
    for j in range(FM.shape[1]):
        ss = scenic_score(FM, i, j, DEBUG=False)
        if ss > max_scenic:
            max_scenic = ss

print(max_scenic)
