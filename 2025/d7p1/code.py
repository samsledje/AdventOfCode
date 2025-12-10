import sys
import numpy as np

CHAR_MAP = {".": 0, "^": 8, "S": 9, "|": 2, "M": 1}

NUM_MAP = {v: k for k, v in CHAR_MAP.items()}

DOWN_SHIFT = [1, 0]
UP_SHIFT = [-1, 0]
RIGHT_SHIFT = [0, 1]
LEFT_SHIFT = [0, -1]


def print_manifold(manifold: np.ndarray, end="#"):
    assert manifold.shape[0] >= 1
    for row in manifold:
        print("".join([NUM_MAP[n] for n in row]))
    print(end * len(row))


def get_positions(manifold: np.ndarray, char: str):
    return np.vstack(np.where(manifold == CHAR_MAP[char])).T


def assign_manifold(manifold: np.ndarray, mask: np.ndarray, char: str):
    manifold[*get_positions(mask, "M").T] = CHAR_MAP[char]


def create_mask(manifold: np.ndarray, positions: np.ndarray):
    mask = np.zeros_like(manifold)
    for pos in positions:
        if (0 <= pos[0] < manifold.shape[0]) and (0 <= pos[1] < manifold.shape[1]):
            mask[*pos] = 1
    return mask


def manifold_step(manifold: np.ndarray):
    start_pos = get_positions(manifold, "S")
    splitter_pos = get_positions(manifold, "^")
    beam_pos = get_positions(manifold, "|")
    free_pos = get_positions(manifold, ".")

    # Beam continues down
    down_beam_mask = (
        create_mask(manifold, start_pos + DOWN_SHIFT)
        | create_mask(manifold, beam_pos + DOWN_SHIFT)
    ) & create_mask(manifold, free_pos)

    # Beam splits
    incoming_beam = create_mask(manifold, splitter_pos + UP_SHIFT) & create_mask(
        manifold, beam_pos
    )
    splitter_with_beams = get_positions(incoming_beam, "M") + DOWN_SHIFT
    new_beams = np.concatenate(
        [splitter_with_beams + LEFT_SHIFT, splitter_with_beams + RIGHT_SHIFT]
    )
    new_beam_mask = create_mask(manifold, new_beams)

    # Update manifold
    assign_manifold(manifold, down_beam_mask, "|")
    assign_manifold(manifold, new_beam_mask, "|")

    # print_manifold(manifold)
    return manifold, len(splitter_with_beams)


if __name__ == "__main__":
    manifold = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            manifold.append([CHAR_MAP[c] for c in line.strip()])
    manifold = np.array(manifold)

    print_manifold(manifold)
    old_manifold = np.zeros_like(manifold)
    while (old_manifold != manifold).any():
        # for _ in range(18):
        old_manifold = manifold.copy()
        manifold, num_splits = manifold_step(manifold)

        # print_manifold(manifold, end="o")
        print_manifold(old_manifold)

    print(num_splits)
