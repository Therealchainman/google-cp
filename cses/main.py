import os,sys
from io import BytesIO, IOBase
from typing import *
import math
from collections import deque, defaultdict


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

class FordFulkersonMaxFlow:
    """
    Ford-Fulkerson algorithm 
    - pluggable augmenting path finding algorithms
    - residual graph
    - bottleneck capacity
    """
    def __init__(self, n: int, edges: List[Tuple[int, int, int]]):
        self.size = n
        self.edges = edges
        self.cap = defaultdict(Counter)
        self.flow = defaultdict(Counter)
        self.adj_list = [[] for _ in range(self.size)]

    def build(self) -> None:
        self.delta = 0
        for src, dst, cap in self.edges:
            self.cap[src][dst] += cap
            self.adj_list[src].append(dst)
            self.adj_list[dst].append(src) # residual edge
            self.delta = max(self.delta, self.cap[src][dst])
        highest_bit_set = self.delta.bit_length() - 1
        self.delta = 1 << highest_bit_set

    def residual_capacity(self, src: int, dst: int) -> int:
        return self.cap[src][dst] - self.flow[src][dst]

    def main_dfs(self, source: int, sink: int) -> int:
        self.build()
        maxflow = 0
        while True:
            self.reset()
            cur_flow = self.dfs(source, sink, math.inf)
            if cur_flow == 0:
                break
            maxflow += cur_flow
        return maxflow

    def neighborhood(self, node: int) -> List[int]:
        return (i for i in self.adj_list[node])

    def dinics_bfs(self, source: int, sink: int) -> bool:
        self.distances = [-1] * self.size
        self.distances[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for nei in self.neighborhood(node):
                if self.distances[nei] == -1 and self.residual_capacity(node, nei) > 0:
                    self.distances[nei] = self.distances[node] + 1
                    queue.append(nei)
        return self.distances[sink] != -1

    def dinics_dfs(self, node: int, sink: int, flow: int) -> int:
        if flow == 0: return 0
        if node == sink: return flow
        while self.ptr[node] < len(self.adj_list[node]):
            nei = self.adj_list[node][self.ptr[node]]
            self.ptr[node] += 1
            if self.distances[nei] == self.distances[node] + 1 and self.residual_capacity(node, nei) > 0:
                cur_flow = self.dinics_dfs(nei, sink, min(flow, self.residual_capacity(node, nei)))
                if cur_flow > 0:
                    self.flow[node][nei] += cur_flow
                    self.flow[nei][node] -= cur_flow
                    return cur_flow
        return 0

    def main_dinics(self, source: int, sink: int) -> int:
        self.build()
        maxflow = 0
        while self.dinics_bfs(source, sink):
            self.ptr = [0] * self.size # pointer to the next edge to be processed (optimizes for dead ends)
            while True:
                cur_flow = self.dinics_dfs(source, sink, math.inf)
                if cur_flow == 0:
                    break
                maxflow += cur_flow
        return maxflow
    
    def general_path_cover(self, source: int, sink: int) -> int:
        self.path, self.paths = [], []
        """
        Since it is possible for there to be a cycle in the graph for the path, that is it could go from node source -> 1 -> 4 -> 1 -> ... -> sink, and that is a valid path
        since it uses disjoint edges to get from source to sink. 
        So if you use a parent array to store prevent cycles, you can get stopped for instance if you go from 1 -> 4 then it won't get back to 1 and could be at dead end.
        You in a sense get stuck in a cycle. 
        But this is already known because the parent array only works for trees or acyclic graphs and not for graphs with cycles.
        So you have to use a set of visited edges (node pairs) to prevent being in cycle for infinite, and because only edge can be used once in a general cover path
        """
        self.vis = set()
        for nei in self.neighborhood(source):
            if self.flow[source][nei] != 1: continue
            self.vis.add((source, nei)) 
            self.path.append(source)
            self.path_dfs(nei, sink)
            self.path.pop()
        return self.paths

    def path_dfs(self, node: int, sink: int) -> None:
        if node == sink:
            self.paths.append([i + 1 for i in self.path + [node]])
            return
        for nei in self.neighborhood(node):
            if (node, nei) in self.vis: continue
            if self.flow[node][nei] == 1:
                self.vis.add((node, nei))
                self.path.append(node)
                self.path_dfs(nei, sink)
                self.path.pop()
                return

def main():
    n, m = map(int, input().split())
    edges = [None] * m
    for i in range(m):
        u, v = map(int, input().split())
        edges[i] = (u - 1, v - 1, 1)
    source, sink = 0, n - 1
    maxflow = FordFulkersonMaxFlow(n, edges)
    mf = maxflow.main_dinics(source, sink)
    print(mf)
    paths = maxflow.general_path_cover(source, sink)
    for path in paths:
        print(len(path))
        print(*path)
    
if __name__ == '__main__':
    main()