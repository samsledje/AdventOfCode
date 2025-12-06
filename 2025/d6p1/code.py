import sys
import numpy as np

OP_MAP = {"+": np.sum, "*": np.prod}

if __name__ == "__main__":
    problems = []
    operations = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            if "+" in line:
                operations = [OP_MAP[i] for i in line.strip().split()]

            else:
                problems.append([int(i) for i in line.strip().split()])

    problems = np.array(problems)
    print(problems)

    running_sum = 0

    for op, nums in zip(operations, problems.T):
        # print(nums, op)
        running_sum += op(nums)

    print(running_sum)
