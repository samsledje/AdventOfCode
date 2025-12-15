import subprocess as sp
import sys
import argparse
import dotenv
import os
from pathlib import Path


def submit(year: int, day: int, part: int, answer: str, token: str) -> None:
    """Submit puzzle answer."""

    raise ValueError("Submit function not implemented yet.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="Year of the puzzle")
    parser.add_argument("day", help="Day of the puzzle")
    parser.add_argument("part", help="Part of the puzzle")
    parser.add_argument("--toy", help="Use toy input", action="store_true")
    parser.add_argument(
        "--autosubmit",
        help="Automatically submit answer. Assumes answer is last line of subprocess output",
        action="store_true",
    )

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

    cmd = f"python -u {code} {inp}"

    proc = sp.Popen(
        cmd.split(),
        stdout=sp.PIPE,
        stderr=sp.STDOUT,
        universal_newlines=True,
        bufsize=1,
    )

    for line in iter(proc.stdout.readline, ""):
        print(line, end="", flush=True)

    puzzle_answer = line.strip()
    proc.stdout.close()
    return_code = proc.wait()
    if return_code:
        sys.exit(return_code)

    if args.autosubmit:
        dotenv.load_dotenv()
        aoc_token = os.getenv("AOC_TOKEN")

        if aoc_token is None:
            raise ValueError(
                "AOC_TOKEN not found in environment variables. Please set it to your Advent of Code session token if you want to use --autosubmit."
            )

        print("Submitting answer...")
        submit(
            year=int(year),
            day=int(day),
            part=int(part),
            answer=puzzle_answer,
            token=aoc_token,
        )
