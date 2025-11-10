"""Day 15 solution."""
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



def main():
   # lines = read_lines(Path(__file__).resolve().parent / 'input/day13.txt')

    genA = 591 #65
    genB = 393 #8921
    factorA = 16807
    factorB = 48271
    count = 0

    for i in range(40000000):
        nextvalA = (genA * factorA) % 2147483647
        nextvalB = (genB * factorB ) % 2147483647
        genA = nextvalA
        genB = nextvalB
        #print("A = ", genA, "  B = ", genB)
        if genA & 0xFFFF == genB & 0xFFFF:
        #    print("Match, i =", i)
            count += 1


    print("Day 15 a = ", count)

    print("Day 15 b = ", 0)

    


if __name__ == "__main__":
    main()
