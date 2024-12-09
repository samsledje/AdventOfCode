import sys
import numpy as np

def checksum(arr):
    pos = np.arange(len(arr))

    checksum = np.sum(arr * pos)
    return checksum

def compress(block_size, free_space, block_id):
    ud = np.concatenate([np.repeat(bid, bs) for bid, bs in zip(block_id, block_size)])
    print(ud)
    cd = []

    for bs, fs in zip(block_size, free_space):
        cd.append(ud[:bs])
        if bs > len(ud):
            break
        ud = np.delete(ud, np.arange(bs))
        cd.append(np.flip(ud[-fs:]))
        ud = np.delete(ud, np.arange(len(ud)-fs, len(ud)))
    #    print(bs,fs, cd, ud)
    #cd.append(ud)
    cd = np.concatenate(cd)
    return cd

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        raw_data = np.array([int(i) for i in f.read().strip()])

    block_size = raw_data[::2]
    free_space = raw_data[1::2]
    block_id = np.arange(len(block_size))

    print(block_size)
    print(block_id)
    print(free_space)

    cd = compress(block_size, free_space, block_id)
    print(cd)
    print(checksum(cd))

