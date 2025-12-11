
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines



def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day5.txt')

   # IDranges = [int,int]
    IDs = []
    IDranges = []
    IDcnt = 0
    RGcnt = 0
  #  print(lines)
    index = 0
    while lines[index].strip() != "":
        #print(lines[index])
        line = lines[index].split("-")
        IDranges.append( (int(line[0]), int(line[1])) )
        #print(line)
        index += 1
  #  print(IDranges)
    index += 1
    while index < len(lines):
  #      print(lines[index])
        IDs.append( int(lines[index]) )
        index += 1

    for ID in IDs:
        for themin, themax in IDranges:
            if themin <= ID <= themax:
                print(f"ID {ID} is in range {themin}-{themax}")
                # how many numbers from ID to themax?
                IDcnt += 1
                break
    print("Day 5 Part 1 = ", IDcnt)
    print("Day 5 Part 2 = ", 0)



if __name__ == "__main__":
    main()
