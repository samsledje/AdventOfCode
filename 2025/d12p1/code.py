import sys
import numpy as np

# Apparantly you can just cheat and check the areas...

# Useful functions
# np.fliplr -> flip left/right
# np.flipud -> flup up/down
# np.rot90(x, k) -> rotate 90' CCW k times (can do negative for CW rot)


def test_region(
    region_size: tuple[int], present_counts: list, presents: dict[np.ndarray]
) -> bool:
    # region = np.ndarray(region_size)
    region_area = region_size[0] * region_size[1]

    present_area = 0
    for pc, pr in zip(present_counts, presents.values()):
        present_area += pr.sum() * pc

    return present_area < region_area


if __name__ == "__main__":
    presents = {}
    regions = []

    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()

        blocks = puzzle_input.strip().split("\n\n")
        present_blocks = blocks[:-1]
        region_block = blocks[-1]

        for pb in present_blocks:
            pb_lines = pb.split("\n")
            assert len(pb_lines) == 4  # assuming all are 3x3
            assert len(pb_lines[-1]) == 3

            present_idx = pb_lines[0].strip(":")
            present_shape = np.zeros((3, 3))

            for i, line in enumerate(pb_lines[1:]):
                for j, char in enumerate(line):
                    if char == "#":
                        present_shape[i, j] = 1
            presents[present_idx] = present_shape

            # print(present_idx)
            # print(present_shape)
            # print("-----")

        for reg in region_block.split("\n"):
            size_str, counts_str = reg.split(":")
            size = [int(i) for i in size_str.split("x")]
            counts = [int(i) for i in counts_str.strip().split()]
            regions.append((size, counts))

            # print(size)
            # print(counts)
            # print("-----")

    num_can_fit = 0
    for rsize, counts in regions:
        num_can_fit += int(test_region(rsize, counts, presents))

    print(num_can_fit)
