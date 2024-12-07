import sys
import os
from pathlib import Path

year, day, part = sys.argv[1:]
os.makedirs(f"{year}/d{day}p{part}", exist_ok=True)
Path(f"{year}/d{day}p{part}/code.py").touch()
Path(f"{year}/d{day}p{part}/input.txt").touch()
Path(f"{year}/d{day}p{part}/toy.txt").touch()

if part == "2":
    # copy code, input, and toy from part 1
    with open(f"{year}/d{day}p1/code.py") as f:
        code = f.read()
    with open(f"{year}/d{day}p1/input.txt") as f:
        data = f.read()
    with open(f"{year}/d{day}p1/toy.txt") as f: 
        toy = f.read()

    with open(f"{year}/d{day}p2/code.py", "w") as f:
        f.write(code)
    with open(f"{year}/d{day}p2/input.txt", "w") as f:
        f.write(data)
    with open(f"{year}/d{day}p2/toy.txt", "w") as f:
        f.write(toy)