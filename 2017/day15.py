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

def partA(genA:int, genB:int, factorA:int, factorB:int) -> int:

    count = 0
    for i in range(40000000):
        nextvalA = (genA * factorA) % 2147483647
        nextvalB = (genB * factorB) % 2147483647
        genA = nextvalA
        genB = nextvalB
        # print("A = ", genA, "  B = ", genB)
        if genA & 0xFFFF == genB & 0xFFFF:
            count += 1

    return count


def partB(genA:int, genB:int, factorA:int, factorB:int) -> int:
    count = 0
#    nextvalA = (genA * factorA) % 2147483647
#    nextvalB = (genB * factorB) % 2147483647

    for i in range(5000000):
        #while nextvalA % 4 != 0:
        while True:
            genA = (genA * factorA) % 2147483647
            if genA % 4 == 0:
                break

        while True:
            genB = (genB * factorB) % 2147483647
            if genB % 8 == 0:
                break

        if(genA & 0xFFFF == genB & 0xFFFF):
            count += 1
    #        print("i = ", i, " A = ", genA, "  B = ", genB)



    return count


def main():
   # lines = read_lines(Path(__file__).resolve().parent / 'input/day13.txt')

    genA = 591
    genB = 393
    factorA = 16807
    factorB = 48271



    print("Day 15 a = ", partA(genA, genB, factorA, factorB))

    print("Day 15 b = ", partB(genA, genB, factorA, factorB))

    


if __name__ == "__main__":
    main()
