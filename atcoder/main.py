import os,sys
from io import BytesIO, IOBase
sys.setrecursionlimit(10**6)
from typing import *

# Fast IO Region
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

from itertools import product
from collections import Counter

def main():
    n, m, k = map(int, input().split())
    arr1, arr2 = [], []
    for _ in range(n):
        arr1.append(tuple(map(int, input().split())))
    for _ in range(m):
        arr2.append(tuple(map(int, input().split())))
    concentrations = []
    concentration = lambda s, w: s/(s + w)*100
    for i, j in product(range(n), range(m)):
        s1, s2 = arr1[i][0], arr2[j][0]
        w1, w2 = arr1[i][1], arr2[j][1]
        s = s1 + s2
        w = w1 + w2
        conc = s/(s + w)*100
        sum_conc = concentration(s1, w1) + concentration(s2, w2)
        conc = concentration(s, w)
        concentrations.append((conc, sum_conc))
    concentrations.sort(reverse=True)
    print(concentrations)
    return concentrations[k - 1]
                    

if __name__ == '__main__':
    print(main())