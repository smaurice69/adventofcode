
from itertools import count
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


def diffchars(st1: str, st2: str) -> int:
    if(len(st1) != len(st2)):
        print("Error in diffchars. Strings not same length")
        exit
    diff = 0
    for i in range(len(st1)):
        if st1[i] != st2[i]:
            diff += 1
    return diff

def diffcharpos(st1: str, st2: str) -> int:
    if(len(st1) != len(st2)):
        print("Error in diffchars. Strings not same length")
        exit
    diff = 0
    pos = 0
    for i in range(len(st1)):
        if st1[i] != st2[i]:
            diff += 1
            pos = i
    return pos



def findbeststring(lines: list) -> tuple[int,int] | None:
    for i in range(len(lines)):  # iterate over all strings
        for j in range(len(lines)):
            if j == i: continue  # no point comparing two identical strings
            if diffchars(lines[i],lines[j]) == 1:
                return i,j
    return 1,2

def main():
    """Run the Day 1 solution."""
    lines = read_lines(Path(__file__).resolve().parent / 'input/day2.txt')

    tot_twos = 0
    tot_threes = 0

    charlist = {}
    for line in lines:
        #print(line)
        charlist.clear()
        for index,ch in enumerate(line):
            if ch not in charlist:
                charlist[ch] = 0          
            charlist[ch] += 1            
        
        count_twos = sum(1 for v in charlist.values() if v == 2)
        count_threes = sum(1 for v in charlist.values() if v == 3)
        if count_twos: tot_twos += 1
        if count_threes: tot_threes += 1
    #    print(charlist, count_twos, count_threes)
    # Convert once
    print("Day 2 a =", tot_twos*tot_threes)

    #lines.sort()
    
    #find strings with only one position differing.

    id1, id2 = findbeststring(lines)
    
    pos = diffcharpos(lines[id1], lines[id2])
       

    print("Day 2 b =", lines[id1][:pos] + lines[id1][pos+1:])
    
if __name__ == "__main__":
    main()
