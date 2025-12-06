import sys
import numpy as np

OP_MAP = {"+": np.sum, "*": np.prod}


def split_line(line, positions):
    last_pos = 0

    parts = []

    for pos in positions:
        parts.append(line[last_pos:pos])
        last_pos = pos + 1
    parts.append(line[last_pos:])
    return parts


def convert_problem(problem_list, operator):
    parts_str = np.array([np.array(list(i)) for i in problem_list]).T
    # print(parts_str)
    nums = [int("".join(r)) for r in parts_str]
    print(nums)
    return operator(nums)


if __name__ == "__main__":
    problems = []
    operations = []

    with open(sys.argv[1], "r") as f:
        file_content = f.read()

    lnum = max([len(i) for i in file_content.split("\n")])
    print(lnum)
    space_columns = set(range(lnum + 1))

    for line in file_content.split("\n"):
        if "+" in line:
            operations = [OP_MAP[i] for i in line.split()]

        else:
            for i, char in enumerate(line):
                if char != " " and i in space_columns:
                    space_columns.remove(i)
    space_columns.remove(lnum)
    print(space_columns)

    array_nums = []
    for line in file_content.split("\n"):
        if ("+" in line) or (line.strip() == ""):
            continue
        just_line = line.ljust(lnum, " ")
        # print(f"#{just_line}#")
        lsplit = split_line(just_line, space_columns)
        # print(lsplit)
        array_nums.append(lsplit)

    running_sum = 0
    for problem_list, op in zip(np.array(array_nums).T, operations):
        running_sum += convert_problem(problem_list, op)

    print(running_sum)
