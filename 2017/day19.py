from os import walk
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

def neighbors(pos, walkable):
    x, y = pos
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nxt = (x + dx, y + dy)
        if nxt in walkable:
            yield nxt




def main():
    #lines = read_lines(Path(__file__).resolve().parent / "input/day19.txt")
    with open(Path(__file__).resolve().parent / "input/day19.txt") as f:
        lines = [line.rstrip("\n") for line in f]
   # print(lines)
    walkable = set()
    locations = {}   # e.g. "A" -> (x, y)

    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch != " ":
                walkable.add((x, y))
                if ch.isalpha():   # A, B, C, ...
                    locations[ch] = (x, y)

    graph = {pos: list(neighbors(pos, walkable)) for pos in walkable}
    letters = []
  #  print(lines)
    # find start
    for x in range(len(lines[0])):
        if lines[0][x] != ' ':
            startx = x
            break
    starty = 0
    direction = 0  # 0 - down, 1 - left, 2 - up, 3 - right
    moved = True
    steps = 0

    while moved == True:
        moved = False
        if direction == 0: #down
            if (startx, starty+1) in walkable: # move down            
                starty += 1
                moved = True
            elif (startx+1,starty) in walkable: # move right
                direction = 3
                startx +=1
                moved = True
            elif (startx-1,starty) in walkable: # move left
                direction = 1
                startx -= 1
                moved = True

        elif direction == 1: #left
            if(startx-1, starty) in walkable: # move left
                startx -= 1
                moved = True
            elif(startx, starty-1) in walkable: # move up
                direction = 2
                starty -= 1
                moved = True
            elif(startx, starty+1) in walkable: # move down
                direction = 0
                starty += 1
                moved = True

        elif direction == 2: # up
            if (startx, starty-1) in walkable: # move up            
                starty -= 1
                moved = True
            elif (startx+1,starty) in walkable: # move right
                direction = 3
                moved = True
                startx +=1
            elif (startx-1,starty) in walkable: # move left
                direction = 1
                startx -= 1
                moved = True

        elif direction == 3: #right
            if(startx+1, starty) in walkable: # move right
                startx += 1
                moved = True
            elif(startx, starty-1) in walkable: # move up
                direction = 2
                starty -= 1
                moved = True
            elif(startx, starty+1) in walkable: # move down
                direction = 0
                starty += 1
                moved = True

       # print(startx,starty)
        if moved: steps += 1
        char = lines[starty][startx]
        if char.isalpha() and moved:            
            letters.append(char)

    print("Day 19 a = ", "".join(letters))
    
  
    
    print("Day 19 b = ", steps+1)


if __name__ == "__main__":
    main()
