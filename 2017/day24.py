from pathlib import Path
import sys
#import threading
#from queue import Queue, Empty
#import time
#from collections import defaultdict
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

#from dataclasses import dataclass
#from typing import List, Optional

#def print_grid2(grid: Grid, posx: int, posy: int) -> None:
def iterdep(comp, input_port):
    best_strength = 0
    best_bridge = []

    comp = tuple(comp)

    @lru_cache(None)
    def dfs(components, port):
        best_strength = 0
        best_bridge = []

        # Turn tuple back to list so your original code still works
        comp_list = list(components)

        for a, b in comp_list:

            if a == port or b == port:

                original = (a, b)

                if b == port:
                    a, b = b, a

                # same behavior as your original version
                remaining = comp_list.copy()
                remaining.remove(original)

                local_strength = a + b

                sub_strength, sub_bridge = dfs(tuple(remaining), b)

                total_strength = local_strength + sub_strength
                total_bridge = [(a, b)] + sub_bridge

                if total_strength > best_strength:
                    best_strength = total_strength
                    best_bridge = total_bridge

        return best_strength, best_bridge

    # initial call uses memoized function
    return dfs(comp, input_port)



def iterdep2(comp, input_port):

    comp = tuple(comp)

    @lru_cache(None)
    def dfs(components, port):
        best_len = 0
        best_strength = 0
        best_bridge = []

        comp_list = list(components)

        for a, b in comp_list:
            if a == port or b == port:

                original = (a, b)

                # orient
                if b == port:
                    a, b = b, a

                # remove used component
                remaining = comp_list.copy()
                remaining.remove(original)

                local_strength = a + b

                sub_len, sub_strength, sub_bridge = dfs(tuple(remaining), b)

                total_len = 1 + sub_len
                total_strength = local_strength + sub_strength
                total_bridge = [(a, b)] + sub_bridge

                # PRIORITY RULE:
                # 1. longer is better
                # 2. if equal length, stronger is better
                if (total_len > best_len or
                    (total_len == best_len and total_strength > best_strength)):
                    best_len = total_len
                    best_strength = total_strength
                    best_bridge = total_bridge

        return best_len, best_strength, best_bridge

    return dfs(comp, input_port)





def main():

        components = []
        lines = read_lines(Path(__file__).resolve().parent / "input/day24.txt")

        for line in lines:
            part1, part2 = line.split('/')
            components.append((int(part1), int(part2)))

        best_strength, best_bridge = iterdep(components, 0)

        print("Day 24 a = ", best_strength)

        best_len, best_strength, best_bridge = iterdep2(components, 0)

       # print("Longest bridge length:", best_len)
       # print("Strength:", best_strength)
       # print("Bridge:", best_bridge)


        print("Day 24 b = ", best_strength)  # placeholder if you’re doing part b later


if __name__ == "__main__":
    main()
