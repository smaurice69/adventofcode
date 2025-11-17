from pathlib import Path
import sys
import threading
from queue import Queue, Empty
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines




def main():
    lines = read_lines(Path(__file__).resolve().parent / "input/day20.txt")

    for line in lines:
   # position
        ppos = line.find("p=<")
        pend = line[ppos:].find(">")
        pstr = line[ppos+3:pend]
        pcrd = pstr.split(",")
    # velocity
        vpos = line.find("v=<")
        vend = line[vpos:].find(">") + vpos
        vstr = line[vpos + 3:vend]
        vcrd = vstr.split(",")
   # accelerarion
        apos = line.find("a=<")
        aend = line[apos:].find(">") + apos
        astr = line[apos + 3:aend]
        acrd = astr.split(",")

        print(pcrd, vcrd, acrd)


    print("Day 20 a = ", 0)
    print("Day 20 b = ", 0)


if __name__ == "__main__":
    main()
