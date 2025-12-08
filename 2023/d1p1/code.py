import sys

if __name__ == "__main__":
    calibrations = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            digits = [i for i in line.strip() if i.isdigit()]
            calibrations.append(int(digits[0] + digits[-1]))
    print(sum(calibrations))
