
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines



def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day2.txt')

    IDs = []
    suminv = 0
    line = lines[0]
    parts = line.split(',')
    for part in parts:
        p1, p2 = part.split('-')
        IDs.append((int(p1), int(p2)))

    for FirstID, SecondID in IDs:
     #   print(f"Processing Rainge ({FirstID}, {SecondID})")
        for i in range(FirstID, SecondID + 1):
            if len(str(i)) % 2 != 0:
                continue
            a = str(i)
            if a[0:len(a) // 2] == a[len(a) // 2:]:
  #              print(a)
                suminv += i

    print("Day 2 Part 1 = ", suminv)



    print("Day 2 Part 2 = ", 0)



if __name__ == "__main__":
    main()
