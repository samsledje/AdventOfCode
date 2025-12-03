import sys
import numpy as np


def compute_pair_joltage(a: int, b: int) -> int:
    return (a * 10) + b


def compute_bank_joltage(bank: np.array) -> int:
    # print(bank)

    pnt_a = np.argmax(bank[:-1])
    pnt_offset = np.argmax(bank[pnt_a + 1 :])
    pnt_b = pnt_a + pnt_offset + 1

    # print(pnt_a, pnt_offset, pnt_b, bank[pnt_a], bank[pnt_b])
    return compute_pair_joltage(bank[pnt_a], bank[pnt_b])


if __name__ == "__main__":
    total_joltage = 0

    with open(sys.argv[1], "r") as f:
        for line in f:
            total_joltage += compute_bank_joltage(
                np.array([int(i) for i in line.strip()])
            )
    print(total_joltage)
