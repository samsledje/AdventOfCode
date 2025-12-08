import sys
import re

DIGIT_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

digit_string = r"\d"
re_string = "({}|{})".format(digit_string, "|".join(DIGIT_WORDS))
matcher = re.compile(re_string)


def to_int(digit):
    if digit.isdigit():
        return digit
    else:
        return str(DIGIT_WORDS.index(digit) + 1)


def isdigit(i):
    return i.isdigit() or (i in DIGIT_WORDS)


if __name__ == "__main__":
    calibrations = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            digits = re.findall(matcher, line)
            calibrations.append(int(to_int(digits[0]) + to_int(digits[-1])))
    print(sum(calibrations))
