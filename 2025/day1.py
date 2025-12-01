
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines



def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day1.txt')

    pos = 50
    zcnt = 0
    passing_zcnt = 0

    for a in lines:
        steps = int(a[1:])
        direction = a[0]

        # count full loops
        passing_zcnt += steps // 100
        partial = steps % 100

        old_pos = pos

        if direction == 'L':
            # detect if partial movement crosses zero
            if partial > 0 and 0 < pos <= partial:
                passing_zcnt += 1

            pos -= partial
            if pos < 0:
                pos = 100 + pos  # <-- remove the extra passing_zcnt += 1 here

        if direction == 'R':
            # detect if partial movement crosses zero
            if partial > 0 and partial >= 100 - pos:
                passing_zcnt += 1

            pos += partial
            if pos > 99:
                pos = pos - 100   # <-- remove the extra passing_zcnt += 1 here

        # your part 1 logic (correct)
        if pos == 0:
            zcnt += 1





    print("Day 1 Part 1 = ", zcnt)
    print("Day 1 Part 2 = ", passing_zcnt)



if __name__ == "__main__":
    main()
