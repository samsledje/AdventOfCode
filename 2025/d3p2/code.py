import sys
import numpy as np

MAX_DETPH = 12


def compute_array_joltage(arr: np.array) -> int:
    return sum(x * 10**i for i, x in enumerate(reversed(arr)))


def recurse_next_best(arr: np.array, depth: int):
    if depth > MAX_DETPH:
        return np.array([])

    argsorted_idx = np.argsort(
        -arr, kind="mergesort"
    )  # ensures smaller indices come first

    # print(f"Depth: {depth} -- array={arr} -- argsorted_idx={argsorted_idx}")
    if not len(argsorted_idx):
        # print("No valid selection found at this depth")
        raise RecursionError()

    for best_idx in argsorted_idx:
        try:
            # print(f"Trying {best_idx} ({arr[best_idx]}) at depth {depth}")
            selected_idx = recurse_next_best(arr[best_idx + 1 :], depth + 1)

            # print(f"Depth: {depth} -- selected_idx={selected_idx}")
            selected_idx += best_idx + 1
            selected_idx = np.concatenate([np.array([best_idx]), selected_idx])

            # print(
            #     f"Depth: {depth} -- selected_idx={selected_idx} -- selected_arr={arr[selected_idx.astype(int)]}"
            # )

            return selected_idx
        except RecursionError:
            continue
    raise RecursionError()


def compute_bank_joltage(bank: np.array) -> int:
    # print(f"Input bank={bank}")
    assert len(bank) > MAX_DETPH

    selected_idx = recurse_next_best(bank, 1)
    selected_batteries = bank[selected_idx.astype(int)]

    # print(f"Selected batteries {selected_batteries}")
    assert len(selected_batteries) == MAX_DETPH
    return compute_array_joltage(selected_batteries)


if __name__ == "__main__":
    total_joltage = 0

    with open(sys.argv[1], "r") as f:
        for i, line in enumerate(f):
            total_joltage += compute_bank_joltage(
                np.array([int(i) for i in line.strip()])
            )
    print(total_joltage)
