import sys

if __name__ == "__main__":
    dial_pos = 50
    num_zeros = 0

    print(f"At position {dial_pos}")

    with open(sys.argv[1], "r") as f:
        for line in f:
            direction = -1 if line[0] == "L" else 1
            distance = int(line[1:])

            print(f"Turn {line[0]} {distance} clicks")

            old_pos = dial_pos
            dial_pos = (old_pos + (direction * distance)) % 100
            zero_passes = abs((old_pos + (direction * distance)) // 100)

            if direction == -1:
                if not old_pos:
                    zero_passes -= 1
                if not dial_pos:
                    zero_passes += 1

            num_zeros += zero_passes

            # print(f"Total zero passes: {num_zeros}")
            print(f"At position {dial_pos}")
            # print(f"New zero passes: {zero_passes}")

    print(num_zeros)
