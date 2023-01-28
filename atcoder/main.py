from typing import List
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

class SegmentTree:
    def __init__(self, n: int, neutral: int, initial_arr: List[int]):
        self.neutral = neutral
        self.size = 1
        self.n = n
        while self.size<n:
            self.size*=2
        self.nodes = [self.neutral for _ in range(self.size*2)] 
        self.build(initial_arr)

    def build(self, initial_arr: List[int]) -> None:
        for i, segment_idx in enumerate(range(self.n)):
            segment_idx += self.size - 1
            self.nodes[segment_idx] = initial_arr[i]
            self.ascend(segment_idx)
    
    def calc_op(self, left: int, right: int) -> int:
        return left + right

    def ascend(self, segment_idx: int) -> None:
        while segment_idx > 0:
            segment_idx -= 1
            segment_idx >>= 1
            left_segment_idx, right_segment_idx = 2*segment_idx + 1, 2*segment_idx + 2
            self.nodes[segment_idx] = self.calc_op(self.nodes[left_segment_idx], self.nodes[right_segment_idx])
        
    def update(self, segment_idx: int, val: int) -> None:
        segment_idx += self.size - 1
        self.nodes[segment_idx] = val
        self.ascend(segment_idx)
            
    def query(self, left: int, right: int) -> int:
        stack = [(0, self.size, 0)]
        result = self.neutral
        while stack:
            # BOUNDS FOR CURRENT INTERVAL and idx for tree
            segment_left_bound, segment_right_bound, segment_idx = stack.pop()
            # NO OVERLAP
            if segment_left_bound >= right or segment_right_bound <= left: continue
            # COMPLETE OVERLAP
            if segment_left_bound >= left and segment_right_bound <= right:
                result = self.calc_op(result, self.nodes[segment_idx])
                continue
            # PARTIAL OVERLAP
            mid_point = (segment_left_bound + segment_right_bound) >> 1
            left_segment_idx, right_segment_idx = 2*segment_idx + 1, 2*segment_idx + 2
            stack.extend([(mid_point, segment_right_bound, right_segment_idx), (segment_left_bound, mid_point, left_segment_idx)])
        return result
    
    def __repr__(self) -> str:
        return f"nodes array: {self.nodes}"
"""

"""
def main():
    n = int(input())
    s = list(input())
    q = int(input())
    unicode = lambda ch: ord(ch) - ord('a')
    # SEGMENT TREE FOR EACH OF THE 26 CHARACTERS REPRESENTED AS INTEGER [0, 25]
    count_seg_trees = [None]*26
    freq_sorted_s = [s.count(chr(i+ord('a'))) for i in range(26)]
    for i in range(26):
        freq_temp = [0]*n
        for j in range(n):
            if unicode(s[j]) == i:
                freq_temp[j] = 1
        count_seg_trees[i] = SegmentTree(n, 0, freq_temp)
    result = []
    """
    checks if sorted based on the frequency of characters in the substring,
    because when you query the segment tree, each query will return frequency of the smallest character first
    for left index to the frequency of this character, now all of the characters should be in that range, 
    because it is supposed to be sorted, if it is not, that means it is not sorted, the other contributing character to the
    frequencey is somewhere else in the substring
    """
    def is_sorted(freq, left):
        for i in range(26):
            if count_seg_trees[i].query(left, left + freq[i]) != freq[i]: return False
            left += freq[i]
        return True
    for _ in range(q):
        query = input().split()
        if query[0] == '1':
            i, c = int(query[1]), query[2]
            i -= 1
            # UPDATE FREQUENCY OF SORTED STRING
            freq_sorted_s[unicode(s[i])] -= 1
            freq_sorted_s[unicode(c)] += 1
            # UPDATE SEGMENT TREE FOR STRING
            count_seg_trees[unicode(s[i])].update(i, 0)
            count_seg_trees[unicode(c)].update(i, 1)
            # UPDATE STRING FOR CHARACTER
            s[i] = c
        else:
            l, r = map(int, (query[1], query[2]))
            l -= 1
            counts = [0]*26
            min_i, max_i = 26, 0
            for i in range(26):
                counts[i] = count_seg_trees[i].query(l, r)
                if counts[i] > 0:
                    min_i = i if min_i == 26 else min_i
                    max_i = i
            check = True
            for i in range(min_i + 1, max_i):
                check &= freq_sorted_s[i] == counts[i]
            # CHECK IF THE SUBSTRING IS SORTED IN ASCENDING ORDER USING SEGMENT TREE QUERIES AND FREQUENCY ARRAY FOR CHARACTERS
            check &= is_sorted(counts, l)
            if check: result.append('Yes')
            else: result.append('No')
    return '\n'.join(result)

if __name__ == '__main__':
    print(main())