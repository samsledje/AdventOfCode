import os
import dotenv
import requests
from pathlib import Path
from argparse import ArgumentParser

HEADERS = {
    "User-Agent": ("github.com/samsledje/Advent-of-Code by samsledje@gmail.com"),
}


def fetch(year: int, day: int, token: str) -> str:
    """Fetch puzzle input."""

    aoc_url = f"https://adventofcode.com/{year}/day/{day}/input"

    response = requests.get(
        url=aoc_url,
        headers=HEADERS,
        cookies={"session": token},
    )
    if not response.ok:
        raise ValueError("Request failed.")

    puzzle_input = response.text.rstrip()
    return puzzle_input


parser = ArgumentParser("Set Up Advent of Code Puzzle")
parser.add_argument("year", help="Year of the puzzle (YYYY)")
parser.add_argument("day", help="Day of the puzzle (1-12)")
parser.add_argument("part", help="Part of the puzzle (1, 2)")

parser.add_argument(
    "--autofetch",
    action="store_true",
    help="Automatically fetch inputs from Advent of Code website",
)

args = parser.parse_args()
year = args.year
day = args.day
part = args.part
autofetch = args.autofetch

assert part in ("1", "2"), "part must be '1' or '2'"
assert day.isdigit() and (1 <= int(day) <= 25), "day must be between 1 and 25"
assert year.isdigit(), "Year must be a number"

year_dir = Path(year)
part_dir = Path(f"{year}/d{day}p{part}")
code_path = part_dir / "code.py"
toy_path = part_dir / "toy.txt"
input_path = part_dir / "input.txt"

if not year_dir.exists():
    print("Welcome to another year of Advent of Code!")
    print(f"Creating directory and README for {year}")
    print("Good luck!")

    os.makedirs(year_dir, exist_ok=True)
    (year_dir / "README.md").touch()

    with open(year_dir / "README.md", "w+") as readme:
        readme.write(f"# Advent of Code {year}")

print(f"Setting up year {year}, day {day}, part {part}")
os.makedirs(part_dir, exist_ok=True)

if autofetch:
    dotenv.load_dotenv()
    aoc_token = os.getenv("AOC_TOKEN")

    if aoc_token is None:
        raise ValueError(
            "AOC_TOKEN not found in environment variables. Please set it to your Advent of Code session token if you want to use --autofetch."
        )

    puzzle_input = fetch(year=int(year), day=int(day), token=aoc_token)

    input_path.write_text(puzzle_input)

if (part == "1") and not code_path.exists():
    print("Creating part 1 template")

    CODE_TEMPLATE = """import sys

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        ... # read input
    """

    code_path.write_text(CODE_TEMPLATE)

if (
    (part == "2")
    and (Path(f"{year}/d{day}p1/code.py").exists())
    and (not code_path.exists())
):
    print("Copying code, input, and toy from part 1 to part 2")

    p1_code = Path(f"{year}/d{day}p1/code.py").read_text()
    p1_data = Path(f"{year}/d{day}p1/input.txt").read_text()
    p1_toy = Path(f"{year}/d{day}p1/toy.txt").read_text()

    code_path.write_text(p1_code)
    input_path.write_text(p1_data)
    toy_path.write_text(p1_toy)

code_path.touch()
input_path.touch()
toy_path.touch()
