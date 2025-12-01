import sys

if __name__ == "__main__":
    dial_pos = 50
    num_zeros = 0

    with open(sys.argv[1], "r") as f:
        for line in f:
            direction = -1 if line[0] == "L" else 1
            distance = int(line[1:])

            print(f"At position {dial_pos}")
            print(f"Turn {line[0]} {distance} clicks")

            dial_pos = (dial_pos + (direction * distance)) % 100
            if not dial_pos:
                num_zeros += 1

    print(f"Ends on {dial_pos}")
    print(num_zeros)
