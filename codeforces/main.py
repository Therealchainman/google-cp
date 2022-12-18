from typing import List
import math
import heapq
from itertools import product

import os,sys
from io import BytesIO, IOBase

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

def bellmanFord(n: int, src: int, edges: List[List[int]]) -> List[int]:
    dist = [math.inf]*n
    dist[src] = 0
    for _ in range(n-1):
        any_relaxed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                any_relaxed = True
                dist[v] = dist[u] + w
        if not any_relaxed: break
    # check for any negative cycles
    for u, v, w in edges:
        if dist[v] > dist[u] + w: return []
    return dist

def dijkstra(n: int, src: int, adj_list: List[List[int]]) -> List[int]:
    dist = [math.inf]*n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in adj_list[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist

def johnsons(n: int, edges: List[List[int]]) -> List[List[int]]:
    # create a new vertex that is connected to all other vertices with weight 0
    # new vertex that will be the source for bellman fourd is going to be n
    # run bellman ford to find shortest paths from the new vertex to all other vertices
    dist = bellmanFord(n+1, n, edges + [[n, i, 0] for i in range(n)])
    if not dist: return [] # if it has negative cycle
    # reweight the edges
    for i in range(len(edges)):
        u, v, w = edges[i]
        edges[i][2] = w + dist[u] - dist[v]
    # run dijkstra for each vertex
    adj_list = [[] for _ in range(n)]
    for u, v, w in edges:
        adj_list[u].append((v, w))
    shortest_paths = [dijkstra(n, i, adj_list) for i in range(n)]
    # undo the reweighting
    for u, v in product(range(n), repeat = 2):
        if shortest_paths == math.inf: continue
        shortest_paths[u][v] = shortest_paths[u][v] + dist[v] - dist[u]
    return shortest_paths

def main():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append([u-1, v-1, w])
    shortest_paths = johnsons(n, edges)
    minVal = math.inf
    for row in shortest_paths:
        for val in row:
            minVal = min(minVal, val)
    return minVal if minVal != math.inf else -math.inf

if __name__ == '__main__':
    t = int(input())
    for _ in range(t):
        print(main())