
from itertools import count
from pathlib import Path
import sys
from collections import defaultdict

from datetime import datetime, date, time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from utils.file_parsers import read_lines

def processpair(c1:str, c2:str) -> bool:
    if len(c1) != 1 or len(c2) != 1:
        raise ValueError("Arguments must be single characters")

    return (c1.lower() == c2.lower()) and (c1 != c2)


def remove2chars(s: str, index: int) -> str:
    if index < 0 or index + 1 >= len(s):
        raise IndexError("Index out of range for removing two characters")
    return s[:index] + s[index+2:]

def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day5.txt')
    newstr = lines[0]

    index = 0
    strlen = len(newstr)
    changed = True

    while changed == True:
        changed = False
        index = 0
        while index < strlen-1:
            res = processpair(newstr[index], newstr[index+1])
            if res:
                newstr = remove2chars(newstr, index)
                strlen = len(newstr)
            #    print(newstr)
                changed = True
            else:
                index += 1



      #  print(f"char1 = {lines[0][i]}, char2 = {lines[0][i+1]}, : {res}")
   # print(newstr)
    print("Day 5 a =", len(newstr))

    print("Day 5 b =", 0)
    
if __name__ == "__main__":
    main()
