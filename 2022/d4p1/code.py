import sys

def contains(r1, r2):
    # r1 contains r2
    (s1, e1) = r1
    (s2, e2) = r2

    return (int(s1) <= int(s2)) and (int(e1) >= int(e2))

def contains_set(r1, r2):
    r1 = range(int(r1[0]), int(r1[1])+1)
    r2 = range(int(r2[0]), int(r2[1])+1)

    r1_contains = (len(set(r2).difference(r1)) == 0)
    r2_contains = (len(set(r1).difference(r2)) == 0)
    return r1_contains or r2_contains

running_sum = 0
with open(sys.argv[1],'r') as f:
    for line in f:
        line = line.strip()
        (r1, r2) = (pair.split('-') for pair in line.split(','))
        if (contains_set(r1, r2) or contains_set(r2, r1)):
            running_sum += 1

print(running_sum)
