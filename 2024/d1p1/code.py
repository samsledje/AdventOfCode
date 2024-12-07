import sys
import numpy as np

with open(sys.argv[1],'r') as f:
    l1, l2 = zip(*[(int(x), int(y)) for x, y in [line.strip().split() for line in f]])
    l1, l2 = np.array(l1), np.array(l2)

    l1sorted, l2sorted = np.sort(l1), np.sort(l2)
    sum_diff = np.sum(np.abs(l1sorted - l2sorted))
    print(sum_diff)