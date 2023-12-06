import sys

def overlaps(r1, r2):
    r1 = range(int(r1[0]), int(r1[1])+1)
    r2 = range(int(r2[0]), int(r2[1])+1)

    return len(set(r1).intersection(r2)) != 0

running_sum = 0
with open(sys.argv[1],'r') as f:
    for line in f:
        line = line.strip()
        (r1, r2) = (pair.split('-') for pair in line.split(','))
        if (overlaps(r1, r2) or overlaps(r2, r1)):
            running_sum += 1

print(running_sum)
