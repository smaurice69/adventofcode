from pathlib import Path
import sys
import threading
from queue import Queue, Empty
import time
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

from dataclasses import dataclass

@dataclass(frozen=True)
class Vec3:
    x: int
    y: int
    z: int

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other: "Vec3") -> "Vec3":
        # Vec3 is frozen (immutable), so we cannot mutate self.
        # Instead, return a NEW Vec3. Python will assign it back to part.vel / part.pos.
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)


# Particle MUST be mutable if you want to do `part.vel += ...` and `part.pos += ...`
@dataclass
class Particle:
    pos: Vec3
    vel: Vec3
    acc: Vec3
    dist: int = 0


def find_duplicates(particles):
    # Map pos → list of indices
    D = defaultdict(list)
    for i, p in enumerate(particles):
        D[p.pos].append(i)

    # Flatten all indexes where duplicates occur
    to_remove = set()
    for idxs in D.values():
        if len(idxs) > 1:     # collision
            to_remove.update(idxs)

    return to_remove

def find_duplicates2(inputlist):
    # Map position -> list of indexes where that position occurs
    D = defaultdict(list)

    for i, p in enumerate(inputlist):
        D[p.pos].append(i)

    # Keep only entries that actually have duplicates
    D = {pos: idxs for pos, idxs in D.items() if len(idxs) > 1}

    return D


def main():
    particles = []
    lines = read_lines(Path(__file__).resolve().parent / "input/day20.txt")

    for line in lines:
        # position
        ppos = line.find("p=<")
        pend = line[ppos:].find(">")
        pstr = line[ppos + 3:pend]
        pcrd = pstr.split(",")

        # velocity
        vpos = line.find("v=<")
        vend = line[vpos:].find(">") + vpos
        vstr = line[vpos + 3:vend]
        vcrd = vstr.split(",")

        # acceleration
        apos = line.find("a=<")
        aend = line[apos:].find(">") + apos
        astr = line[apos + 3:aend]
        acrd = astr.split(",")

        pp = Vec3(int(pcrd[0]), int(pcrd[1]), int(pcrd[2]))
        vp = Vec3(int(vcrd[0]), int(vcrd[1]), int(vcrd[2]))
        ap = Vec3(int(acrd[0]), int(acrd[1]), int(acrd[2]))
        p = Particle(pp, vp, ap)
        particles.append(p)

    minacc = sys.maxsize
    theindex = None

    for idx, p in enumerate(particles):
        tacc = abs(p.acc.x) + abs(p.acc.y) + abs(p.acc.z)
        if tacc < minacc:
            minacc = tacc
            theindex = idx

    print("Day 20 a = ", theindex)

    # Example: calling duplicates on positions
  #  duplicates = find_duplicates(particles)
  #  print("Duplicate positions (pos -> indices):", duplicates)

    # If you uncomment your simulation, this now works:
    for i in range(100):
        for j in range(len(particles)):
             part = particles[j]
             part.vel += part.acc
             part.pos += part.vel
        
             
        to_remove = find_duplicates(particles)
        if to_remove:
            #print("Removing:", to_remove)
            # Remove all collided particles
            particles = [p for idx, p in enumerate(particles) if idx not in to_remove]
            #print("Sizeof particles = ", len(particles))
        #if len(duplicates) > 0:
        #    print("Duplicates = ", duplicates)

    print("Day 20 b = ", len(particles))


if __name__ == "__main__":
    main()
