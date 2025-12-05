import sys
import numpy as np


def check_fresh(x: int, ranges: np.array):
    gt_range = x >= ranges[:, 0]
    lt_range = x <= ranges[:, 1]
    in_range = gt_range & lt_range
    return in_range.any().astype(int)


if __name__ == "__main__":
    fresh_ranges = []
    available_products = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            if line.strip() == "":
                break

            start, end = line.split("-")
            fresh_ranges.append((int(start), int(end)))

        for line in f:
            available_products.append(int(line.strip()))

    fresh_ranges = np.array(fresh_ranges)
    # print(fresh_ranges)
    # print(available_products)

    num_fresh = 0
    for p in available_products:
        is_fresh = check_fresh(p, fresh_ranges)
        # print(p, is_fresh)
        num_fresh += is_fresh
    print(num_fresh)
