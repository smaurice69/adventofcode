
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


def main():
    """Run the Day 1 solution."""
    lines = read_lines(Path(__file__).resolve().parent / 'input/day1test.txt')

    freq = 0
    for a in lines:
        freq += int(a)

    index = 0
    freqs = [0]

    while True:
        a = int(lines[index])
        curfreq = freqs[index]
        newfreq = curfreq + a
        print("Newfreq = ", newfreq)
        if newfreq in freqs:
            print("duplicate ")
            break
        else:
            freqs.append(newfreq)
        index += 1
        if index == len(lines):
            index = 0
            print("Restart list")





    print ("Day 1 a = ", freq)

    print ("Day 1 b = ", newfreq)
    


if __name__ == "__main__":
    main()
