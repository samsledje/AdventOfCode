import sys
import re


def check_number_valid(x: str):
    substrings = [x[:i] for i in range(1, (len(x) // 2) + 1)]
    for ss in substrings:
        m = re.match(f"^({ss})+$", x)
        if m is not None:
            print(f"Matched full string: {x}, substring: {ss}")
            return False
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
                invalid_sum += x

    print(invalid_sum)
