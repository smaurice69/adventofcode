
from itertools import count
from pathlib import Path
import sys
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day3.txt')

    grid = defaultdict(lambda: defaultdict(int))  # default int = 0
    grid2 = defaultdict(lambda: defaultdict(set))
    all_ids = set()

    for line in lines:
        parts = line.split()

        item = int(parts[0][1:]) # Remove '#' and convert to int
        all_ids.add(item)

        pos = parts[2][:-1]  # Remove ':' at the end
        poscord = pos.split(',')
        posx = int(poscord[0])
        posy = int(poscord[1])

        size = parts[3]
        sizecord = size.split('x')
        sizex = int(sizecord[0])
        sizey = int(sizecord[1])

        for x in range(posx, posx + sizex):
            for y in range(posy, posy + sizey):
                grid[x][y] += 1
                grid2[x][y].add(item)

       # print(item, posx, posy, sizex, sizey)

       # print(parts)
    multicells = 0
    candidates = set(all_ids)  # start assuming all are non-overlapping

    for r, row in grid.items():
        for c, value in row.items():
            if value > 1:
                multicells += 1
                 # every ID in this cell overlaps
                for claim_id in grid2[r][c]:
                    if claim_id in candidates:
                        candidates.remove(claim_id)

    uniqueID = candidates.pop() if len(candidates) == 1 else -1

    print("Day 3 a =", multicells)

    print("Day 3 b =", uniqueID)
    
if __name__ == "__main__":
    main()
