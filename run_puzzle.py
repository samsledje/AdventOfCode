import subprocess as sp
import sys
import argparse
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="Year of the puzzle")
    parser.add_argument("day", help="Day of the puzzle")
    parser.add_argument("part", help="Part of the puzzle")
    parser.add_argument("--toy", help="Use toy input", action="store_true")

    args = parser.parse_args()
    year = args.year
    day = args.day
    part = args.part

    code = Path(f"{year}/d{day}p{part}/code.py")

    if args.toy:
        inp = Path(f"{year}/d{day}p{part}/toy.txt")
    else:
        inp = Path(f"{year}/d{day}p{part}/input.txt")

    assert code.exists(), f"{code} does not exist"
    assert inp.exists(), f"{inp} does not exist"

    cmd = f"python {code} {inp}"

    proc = sp.Popen(cmd.split(), stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = proc.communicate()
    print(out.decode(), end="")
    if err is not None:
        print(err.decode())
