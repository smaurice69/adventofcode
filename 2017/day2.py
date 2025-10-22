"""Day 2 solution."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day2.txt')

    
    tmpsum = 0

    for line in lines:
        vector = list(map(int, line.split()))
        minval = min(vector)
        maxval = max(vector)
        tmpsum += (maxval - minval)


    print ("Day 2 a = ", tmpsum)

    lines = read_lines(Path(__file__).resolve().parent / 'input/day2.txt')

    
    tmpsum = 0
    for line in lines:
        vector = list(map(int, line.split()))
        vector.sort(reverse=True)
        for i in range(len(vector)):
            for j in range(i+1, len(vector)):
                if vector[i] % vector[j] == 0:
                    tmpsum += vector[i] // vector[j]
                    break
            
    print ("Day 2 b = ", tmpsum)

if __name__ == "__main__":
    main()
