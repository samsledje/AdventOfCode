import sys

class Directory:
    def __init__(self,name,parent):
        self._name = name
        self._children = {}
        self._parent = parent

    def name(self):
        return self._name

    def children(self):
        return self._children

    def add_child(self, x):
        self._children[x.name()] = x

    def has_child(self, n):
        return n in self._children.keys()

    def get_child(self, n):
        return self._children[n]

    def size(self):
        return sum([c.size() for c in self._children.values()])

    def parent(self):
        return self._parent

    def __repr__(self):
        s = ''
        s += f'[DIR] {self._name} {self.size()}\n'
        for c in self._children.values():
            s += f'{str(c)}\n'
        s += f'[END DIR] {self._name}'
        return s

    def size_below(self, SIZE_THRESH):
        si = 0
        if self.size() < SIZE_THRESH:
            si += self.size()
        for c in self._children.values():
            if isinstance(c, Directory):
                si += c.size_below(SIZE_THRESH)
        return si

class File:
    def __init__(self,name,size):
        self._name = name
        self._size = size

    def name(self):
        return self._name

    def size(self):
        return self._size

    def __repr__(self):
        return f'[FILE] {self._name} {self._size}'

MAX_SIZE = 100000
ROOT_DIR = Directory('/', None)

CWD = ROOT_DIR

with open(sys.argv[1],'r') as f:
    for line in f:
        if line.startswith('$ cd'):
            target_dir = line.split()[2]
            if target_dir== '..':
                CWD = CWD.parent()
            elif target_dir == '/':
                CWD = ROOT_DIR
            else:
                assert CWD.has_child(target_dir), (CWD, target_dir)
                CWD = CWD.get_child(target_dir)
        elif line.startswith('$ ls'):
            continue
        elif line.startswith('dir'):
            d_name = line.split()[1]
            if not CWD.has_child(d_name):
                new_d = Directory(d_name, CWD)
                CWD.add_child(new_d)
        else:
            f_size, f_name = line.split()
            if not CWD.has_child(f_name):
                new_f = File(f_name, int(f_size))
                CWD.add_child(new_f)

CWD = ROOT_DIR
print(ROOT_DIR.size_below(MAX_SIZE))
