"""Day 1 solution."""

#from calendar import c
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


def main():
    """Run the Day 1 solution."""
    lines = read_lines(Path(__file__).resolve().parent / 'input/day1.txt')

    num = lines[0]
    tmpsum = 0

    for i in range(len(num)):
        if num[i] == num[(i + 1) % len(num)]:
            tmpsum += int(num[i])

    print ("Day 1 a = ", tmpsum)
    
    tmpsum = 0

    for i in range(len(num)):
        if num[i] == num[(i+len(num)//2) % len(num)]:
            tmpsum += int(num[i])

    print ("Day 1 b = ", tmpsum)
    


if __name__ == "__main__":
    main()
