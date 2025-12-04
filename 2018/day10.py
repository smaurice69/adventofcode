
from itertools import count
from pathlib import Path
from pickletools import read_decimalnl_short
import sys
from collections import defaultdict
from collections import Counter
import shutil

from datetime import datetime, date, time
import re


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


def extract_parenthesis_contents(s: str):
    # Matches anything inside (), [], {}, or <>
    pattern = r'\((.*?)\)|\[(.*?)\]|\{(.*?)\}|<(.*?)>'
    results = []

    for match in re.findall(pattern, s):
        # `match` is a tuple of 4 slots (one for each type), only one will be non-empty
        for group in match:
            if group:
                results.append(group)
    return results


def print_poslist(poslist):
    """
    Render points sparsely but with full spacing preserved.
    Does NOT allocate a huge grid.
    Streams line by line.
    """

    if not poslist:
        print("<empty>")
        return

    pts = set(poslist)

    xs = [x for x, _ in pts]
    ys = [y for _, y in pts]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # For each row in the bounding box, print only if needed
    for y in range(min_y, max_y + 1):

        # Check if row contains any points
        row_points = [xv for (xv, y2) in pts if y2 == y]

        if not row_points:
            # Skip empty rows entirely?
            # For AoC Day 10 you MUST print empty rows too.
            print("." * (max_x - min_x + 1))
            continue

        # Build row: only print needed segment
        row = []
        rp = set(row_points)
        for x in range(min_x, max_x + 1):
            row.append("#" if x in rp else ".")

        print("".join(row))


def count_islands(poslist):
    pts = set(poslist)
    visited = set()
    islands = 0

    # Choose connectivity (4-neighbors or 8-neighbors)
    # 4-connected: up/down/left/right
    # 8-connected: diagonals as well
    dirs = [(1,0), (-1,0), (0,1), (0,-1),
            (1,1), (1,-1), (-1,1), (-1,-1)]  # comment out last 4 for 4-connectivity

    for p in pts:
        if p in visited:
            continue

        # New island found
        islands += 1
        stack = [p]

        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))

            # explore neighbors
            for dx, dy in dirs:
                n = (x + dx, y + dy)
                if n in pts and n not in visited:
                    stack.append(n)

    return islands


def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day10.txt')
    
    poslist = []
    vellist = []
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    minarea = 100000000000



    for line in lines:
        parsed_line = extract_parenthesis_contents(line)
        pos = parsed_line[0].split(",")
        posx = int(pos[0])
        posy = int(pos[1])        
        vel = parsed_line[1].split(",")
        velx = int(vel[0])
        vely = int(vel[1])

        poslist.append( (posx, posy) )
        vellist.append( (velx, vely) )  

     ####

     THIS SOLUTION DOES not WORK FULLY YET

     #####


    for t in range(11000):      # <-- real input needs thousands of seconds
        for i in range(len(poslist)):
            poslist[i] = (poslist[i][0] + vellist[i][0], poslist[i][1] + vellist[i][1])

        print(f"After {t} seconds: {count_islands(poslist)} islands")

   
    print("Day 10 a =", 0)
    print("Day 10 b =", 0)
    
if __name__ == "__main__":
    main()
