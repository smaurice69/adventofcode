
from itertools import count
from pathlib import Path
from pickletools import read_decimalnl_short
import sys
from collections import defaultdict
from collections import Counter

from datetime import datetime, date, time
import re

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

# given a list of x,y coordinates. Genereate a list of areas for each x,y pair that is only limited by other x,y pairs

def count_frequencies(pairs):

    # Build bounding box
    xs = [x for (_, x, _) in pairs]
    ys = [y for (_, _, y) in pairs]

    xmin = min(xs) - 10
    xmax = max(xs) + 10
    ymin = min(ys) - 10
    ymax = max(ys) + 10

    pts = [(letter, x, y) for (letter, x, y) in pairs]
    orig_pos = {(x, y): letter for (letter, x, y) in pts}

    counter = Counter()
    infinite = set()     # <- NEW: store IDs with infinite areas

    for y in range(ymin, ymax+1):
      #  if y % 50 == 0:
      #      print(f"Processing row y={y}")
        for x in range(xmin, xmax+1):

            # Skip original point itself
            if (x, y) in orig_pos:
                continue

            # Compute all distances
            distances = []
            for letter, px, py in pts:
                dist = abs(px - x) + abs(py - y)
                distances.append((dist, letter))

            distances.sort(key=lambda t: t[0])

            # Ties: no assignment
            if distances[0][0] == distances[1][0]:
                continue

            closest_id = distances[0][1]

            # If we are on the boundary: infinite area
            if x == xmin or x == xmax or y == ymin or y == ymax:
                infinite.add(closest_id)
            else:
                counter[closest_id] += 1

    # Remove infinite regions
    for inf_id in infinite:
        if inf_id in counter:
            del counter[inf_id]

    return counter

def region_size(pairs, limit:int):

    # Build bounding box
    xs = [x for (_, x, _) in pairs]
    ys = [y for (_, _, y) in pairs]

    xmin = min(xs) - 100
    xmax = max(xs) + 100
    ymin = min(ys) - 100
    ymax = max(ys) + 100
    regcnt = 0
    for y in range(ymin,ymax+1):
    #    print(f"Processing row y={y}")
        for x in range(xmin,xmax+1):
            # Compute all distances
            total_distance = 0
            for letter, px, py in pairs:
                dist = abs(px - x) + abs(py - y)
                total_distance += dist
            
            if(total_distance < limit):
                regcnt += 1

    return regcnt


def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day6.txt')

    pairs = []
    id = 0

    for s in lines:
        a, b = map(int, re.split(r"\s*,\s*", s))
        pair_id = id
        pairs.append([pair_id,a,b])
        id += 1
    
    counts = count_frequencies(pairs)
    largest = counts.most_common(1)[0][1]


    part2 = region_size(pairs, 10000)


    print("Day 6 a =", largest+1)

    print("Day 6 b =", part2)
    
if __name__ == "__main__":
    main()
