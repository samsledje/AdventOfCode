import sys

calList = []

with open(sys.argv[1],'r') as f:

    running_sum = 0
    for line in f:
        l = line.strip()

        if l == '':
            calList.append(running_sum)
            running_sum = 0
        else:
            running_sum += int(l)

print(max(calList))
