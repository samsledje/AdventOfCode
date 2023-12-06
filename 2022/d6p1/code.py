import sys

BUFFER_SIZE = 4

def test_buffer(b):
    assert len(b) == BUFFER_SIZE
    bset = set(b)
    return len(bset) == len(b)

with open(sys.argv[1],'r') as f:
    inp_stream = f.read().strip()

N = len(inp_stream)
for pos in range(N-BUFFER_SIZE+1):
    buf = inp_stream[pos:pos+BUFFER_SIZE]
    if test_buffer(buf):
        print(pos+BUFFER_SIZE)
        break

