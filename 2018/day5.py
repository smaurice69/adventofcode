
from itertools import count
from pathlib import Path
import sys
from collections import defaultdict

from datetime import datetime, date, time


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


#from future.types import newstr


from utils.file_parsers import read_lines

def processpair(c1:str, c2:str) -> bool:
    if len(c1) != 1 or len(c2) != 1:
        raise ValueError("Arguments must be single characters")

    return (c1.lower() == c2.lower()) and (c1 != c2)


def remove2chars(s: str, index: int) -> str:
    if index < 0 or index + 1 >= len(s):
        raise IndexError("Index out of range for removing two characters")
    return s[:index] + s[index+2:]

def reduce_string(s: str) -> str:
    """Apply pair-removal rules repeatedly until stable."""
    newstr = s
    strlen = len(newstr)
    index = 0
    changed = True

    while changed:
        changed = False
        index = 0

        while index < strlen - 1:
            if processpair(newstr[index], newstr[index + 1]):
                newstr = remove2chars(newstr, index)
                strlen -= 2
                changed = True

                # move back one step to catch new reactions
                if index > 0:
                    index -= 1
            else:
                index += 1

    return newstr

def remove_letter(s: str, ch: str) -> str:
    if len(ch) != 1 or not ch.islower():
        raise ValueError("Second argument must be a single lowercase letter")

    lower = ch
    upper = ch.upper()

    return ''.join(c for c in s if c != lower and c != upper)



def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day5.txt')
    newstr = lines[0]

    newstr = reduce_string(newstr)

    print("Day 5 a =", len(newstr))

    newstr = lines[0]
    max_letter = max(c.lower() for c in newstr if c.isalpha())
   # print(max_letter)
    minlen = len(newstr)

    original = lines[0]

    for i in range(ord('a'), ord(max_letter) + 1):
      #  newstr = lines[0]
        newstr = remove_letter(original, chr(i))
     #   print(newstr)
        newstr = reduce_string(newstr)
        if len(newstr) < minlen:
            minlen = len(newstr)
    print("Day 5 b =", minlen)
    
if __name__ == "__main__":
    main()
