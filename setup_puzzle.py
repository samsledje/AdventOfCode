import sys
import os
from pathlib import Path

try:
    year, day, part = sys.argv[1:]
except ValueError:
    print("Usage: python setup_puzzle.py [year] [day] [part]")
    sys.exit(0)

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

if (part == "1") and not code_path.exists():
    print("Creating part 1 template")

    CODE_TEMPLATE = """import sys

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        ... # read input
    """

    with open(code_path, "w") as f:
        f.write(CODE_TEMPLATE)

if (
    (part == "2")
    and (Path(f"{year}/d{day}p1/code.py").exists())
    and (not code_path.exists())
):
    print("Copying code, input, and toy from part 1 to part 2")

    # copy code, input, and toy from part 1
    with open(f"{year}/d{day}p1/code.py") as f:
        code = f.read()
    with open(f"{year}/d{day}p1/input.txt") as f:
        data = f.read()
    with open(f"{year}/d{day}p1/toy.txt") as f:
        toy = f.read()

    with open(code_path, "w") as f:
        f.write(code)
    with open(input_path, "w") as f:
        f.write(data)
    with open(toy_path, "w") as f:
        f.write(toy)

code_path.touch()
input_path.touch()
toy_path.touch()
