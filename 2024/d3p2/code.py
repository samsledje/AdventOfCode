import sys
import re

mul_re = re.compile("mul\((\d+),(\d+)\)")

if __name__ == "__main__":
    file = sys.argv[1]
    with open(file) as f:
        line = f.read()

    init_chunks = line.split("do()")
    do_chunks = []
    for c in init_chunks:
        do_chunks.append(c.split("don't()")[0])
    # print(do_chunks)

    muls = []
    for c in do_chunks:
        muls.extend(re.findall(mul_re, c))
    result = sum([int(a) * int(b) for a, b in muls])
    print(result)