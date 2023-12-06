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
        line1 = line.strip()
        line2 = f.readline().strip()
        line3 = f.readline().strip()

        badge = set(line1).intersection(line2).intersection(line3)
        assert len(badge) == 1
        badge = list(badge)[0]

        running_sum += get_priority(badge)

print(running_sum)
