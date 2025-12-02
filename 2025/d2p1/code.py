import sys


def check_number_valid(x: str):
    if len(x) % 2:
        return True
    else:
        first_part = x[: len(x) // 2]
        second_part = x[len(x) // 2 :]
        if first_part == second_part:
            # print(f"After split: {first_part}, {second_part}")
            return False
        else:
            return True


if __name__ == "__main__":
    ranges = []

    with open(sys.argv[1], "r") as f:
        line = f.readline().strip()

    for rng in line.split(","):
        start, end = rng.split("-")
        ranges.append((int(start), int(end)))

    # print(ranges)

    invalid_sum = 0

    for rng in ranges:
        for x in range(int(rng[0]), int(rng[1]) + 1):
            if not check_number_valid(str(x)):
                # print(x)
                invalid_sum += x

    print(invalid_sum)
