import sys
import numpy as np


if __name__ == "__main__":
    fresh_ranges = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            if line.strip() == "":
                break

            start, end = line.split("-")
            fresh_ranges.append((int(start), int(end)))

    fresh_ranges = np.array(fresh_ranges)
    lexsort = np.lexsort((fresh_ranges[:, 1], fresh_ranges[:, 0]))
    sorted_ranges = fresh_ranges[lexsort]

    ## Worked on toy example, unable to allocate 3.99 PiB for input :)
    # max_id = np.max(fresh_ranges)
    # possible_ids = np.arange(1, max_id + 1)

    # gt_check = possible_ids[:, None] >= fresh_ranges[:, 0]
    # lt_check = possible_ids[:, None] <= fresh_ranges[:, 1]
    # in_check = gt_check & lt_check
    # fresh_check = np.any(in_check, 1)
    # print(np.sum(fresh_check))
    #####

    num_fresh = 0

    last_r_0, last_r_1 = 0, 0
    for r_0, r_1 in sorted_ranges:
        assert r_0 <= r_1
        assert r_0 >= last_r_0

        range_size = r_1 - r_0 + 1

        if r_0 <= last_r_1:
            if r_1 <= last_r_1:
                rtype = "contained"
                new_fresh = 0
            else:
                rtype = "overlap"
                new_fresh = r_1 - last_r_1
                last_r_1 = r_1
        else:
            rtype = "discrete"
            new_fresh = range_size
            last_r_1 = r_1
        last_r_0 = r_0

        num_fresh += new_fresh
        # print(
        #     f"({r_0:>15}, {r_1:>15}) [{rtype:<10}] added \t{new_fresh:>15} \tnew fresh products (total {num_fresh})"
        # )

    print(num_fresh)
