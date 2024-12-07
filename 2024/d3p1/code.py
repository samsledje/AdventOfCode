import sys
import re

mul_re = re.compile("mul\((\d+),(\d+)\)")

if __name__ == "__main__":
    file = sys.argv[1]
    with open(file) as f:
        line = f.read()

    mul_instructions = re.findall(mul_re, line)
    result = sum([int(a) * int(b) for a, b in mul_instructions])
    print(result)