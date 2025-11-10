"""Day 14 solution."""
import copy
import numbers
from pathlib import Path
import sys
import re
from collections import deque

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

def reverse_circular(lst, start, length):
    n = len(lst)
    for i in range(length // 2):
        a = (start + i) % n
        b = (start + length - 1 - i) % n
        lst[a], lst[b] = lst[b], lst[a]
    return lst

def knot_hash(s: str) -> str:
    """
    Compute the Knot Hash (Advent of Code 2017, Day 10 part 2) for the given string.
    Returns a 32-character lowercase hex digest.
    """
    # Convert to ASCII codes + standard suffix
    lengths = [ord(c) for c in s] + [17, 31, 73, 47, 23]
    # Sparse hash over 64 rounds
    numbers = list(range(256))
    current_position = 0
    skip_size = 0
    for _ in range(64):
        for length in lengths:
            reverse_circular(numbers, current_position, length)
            current_position = (current_position + length + skip_size) % 256
            skip_size += 1
    # Dense hash: XOR each block of 16
    dense = []
    for i in range(0, 256, 16):
        x = 0
        for v in numbers[i:i+16]:
            x ^= v
        dense.append(x)
    # Hex digest
    return ''.join(f'{b:02x}' for b in dense)

def hex_to_binary(hex_str: str) -> str:
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)

def count_clusters_grid(grid, diag=False):
    """
    grid: list[str] of length H (e.g., 128), each string of '0'/'1' of length W (e.g., 128)
    diag: False for 4-neighbors, True for 8-neighbors
    """
    H, W = len(grid), len(grid[0])
    visited = [[False]*W for _ in range(H)]
    clusters = 0

    if diag:
        nbrs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    else:
        nbrs = [(-1,0),(1,0),(0,-1),(0,1)]

    for r in range(H):
        for c in range(W):
            if grid[r][c] == '1' and not visited[r][c]:
                clusters += 1
                dq = deque([(r,c)])
                visited[r][c] = True
                while dq:
                    rr, cc = dq.popleft()
                    for dr, dc in nbrs:
                        nr, nc = rr+dr, cc+dc
                        if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc] and grid[nr][nc] == '1':
                            visited[nr][nc] = True
                            dq.append((nr,nc))
    return clusters




def main():
   # lines = read_lines(Path(__file__).resolve().parent / 'input/day13.txt')
    thelist: list[str] = []
    totcnt = 0
    for i in range(128):
        istring = "nbysizxe-"+str(i)
        tmpstring = hex_to_binary(knot_hash(istring))
       # print(tmpstring)
        usecnt = 0
        for c in tmpstring:
            if c == '1':
                usecnt += 1
        totcnt += usecnt
        thelist.append(tmpstring)
    print("Day 14 a = ", totcnt)

    numgrps = count_clusters_grid(thelist)
    print("Day 14 b=", numgrps)

    


if __name__ == "__main__":
    main()
