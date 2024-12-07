import sys
import numpy as np

with open(sys.argv[1],'r') as f:
    l1, l2 = zip(*[(int(x), int(y)) for x, y in [line.strip().split() for line in f]])
    l1, l2 = np.array(l1), np.array(l2)

    ss = 0
    for i in l1:
        incidence = np.sum(l2 == i)
        ss += (incidence * i)
    print(ss)