import sys

def get_priority(x):
    x = ord(x)
    return x - (int(x > 96.5) * 96) - (int(x < 96.5) * 38)

def split_list(l):
    half = len(l) // 2

    first_half = l[:half]
    second_half = l[-half:]
    return first_half, second_half

running_sum = 0
with open(sys.argv[1],'r') as f:
    for line in f:
        line = line.strip()
        first, second = split_list(line)
        dupSet = set(first).intersection(set(second))
        assert len(dupSet) == 1
        dup = list(dupSet)[0]
        running_sum += get_priority(dup)

print(running_sum)
