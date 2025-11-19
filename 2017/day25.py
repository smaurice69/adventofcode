from pathlib import Path
import sys
#import threading
#from queue import Queue, Empty
#import time
#from collections import defaultdict
#from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

#from dataclasses import dataclass
#from typing import List, Optional

#def print_grid2(grid: Grid, posx: int, posy: int) -> None:



def main():

        lines = read_lines(Path(__file__).resolve().parent / "input/day24.txt")

        for line in lines:
            part1, part2 = line.split('/')
            components.append((int(part1), int(part2)))

        print("Day 25 a = ", 0)

if __name__ == "__main__":
    main()
