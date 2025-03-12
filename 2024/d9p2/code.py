import sys
import numpy as np

def checksum(arr):
    pos = np.arange(len(arr))
    mult_pos = (arr * pos)
    checksum = np.sum(mult_pos[np.where(mult_pos >= 0)])

    return checksum

def compress(block_size, free_space, block_id):
    ud = np.concatenate([np.concatenate([np.repeat(bid, bs), (-1 * np.ones(fs))])  for (bid, bs), fs in zip(zip(block_id, block_size), free_space)])
    ud = np.concatenate([ud, np.repeat(block_id[-1], block_size[-1])])

    total_size = np.sum(block_size)

    print(ud)
    cd = []

    i = 0
    while len(cd) < total_size:
        element = ud[i]

        if element != -1:
            cd.append(element)
        else:

            # strip all gaps from the end
            while ud[-1] == -1:
                # print("stripping from end")
                ud = np.delete(ud, -1)
            
            # grab the last real block
            element = ud[-1]
            cd.append(element)
            ud = np.delete(ud, -1)
            # print(f"updated ud to {ud}")
        
        # print(cd)
        i += 1

    return cd

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        raw_data = np.array([int(i) for i in f.read().strip()])
    # print(raw_data)

    block_size = raw_data[::2]
    free_space = raw_data[1::2]
    block_id = np.arange(len(block_size))

    # print(block_id)
    # print(block_size)
    # print(free_space)
    # print(block_id)

    # cd = compress(block_size, free_space, block_id)
    cd = np.array([0,0,9,9,2,1,1,1,7,7,7,-1,4,4,-1,3,3,3,-1,-1,-1,-1,5,5,5,5,-1,6,6,6,6,-1,-1,-1,-1,-1,8,8,8,8,-1,-1])
    # print(cd)


    print(checksum(cd))

