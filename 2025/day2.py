
from pathlib import Path
from pprint import isreadable
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines
from utils.utils import is_prime

def part1(IDs: list[tuple[int, int]]) -> int:
    suminv = 0
    for FirstID, SecondID in IDs:     
        for i in range(FirstID, SecondID + 1):
            if len(str(i)) % 2 != 0:
                continue
            a = str(i)
            if a[0:len(a) // 2] == a[len(a) // 2:]:
                  suminv += i
    return suminv

def is_repetition(s: str) -> bool:
    return s in (s + s)[1:-1]


def part2(IDs: list[tuple[int, int]]) -> int:
    suminv = 0
    for FirstID, SecondID in IDs:     
    #    print(f"Processing Rainge ({FirstID}, {SecondID})")
        for i in range(FirstID, SecondID + 1):             
            thelen = len(str(i))
            thenum = str(i)
            #if(len(set(str(i))) <= 1):
                #print(f"Found all identical = {i}")
            
            if is_repetition(thenum):
           #     print(i)
                suminv += i
                continue


            elif is_prime(thelen):
            #    print(f"Lengith is prime = {i}")
                continue
            #else:
                #print(f"Not handled = {i}")

            #substring length 2 -> substring length len//2



    return suminv






def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day2.txt')

    IDs = []
    suminv = 0
    line = lines[0]
    parts = line.split(',')
    for part in parts:
        p1, p2 = part.split('-')
        IDs.append((int(p1), int(p2)))

    

    print("Day 2 Part 1 = ", part1(IDs))



    print("Day 2 Part 2 = ", part2(IDs))



if __name__ == "__main__":
    main()
