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

n_viz = 0
for i in range(FM.shape[0]):
    for j in range(FM.shape[1]):
        #print(i, j, FM[i,j], is_visible(FM, i, j, DEBUG=False))
        if is_visible(FM, i, j):
            n_viz += 1
print(n_viz)
