from pathlib import Path
import sys
import threading
from queue import Queue, Empty
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

from dataclasses import dataclass

@dataclass
class Vec3:
    x: int
    y: int
    z: int

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other: "Vec3") -> "Vec3":
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

@dataclass
class Particle:
    pos: Vec3
    vel: Vec3
    acc: Vec3
    dist: int = 0



def main():
    particles = []
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
     #   print(pcrd, vcrd, acrd)

    minacc = sys.maxsize

    for idx, p in enumerate(particles):
        tacc = abs(p.acc.x) + abs(p.acc.y)+abs(p.acc.z)
    #    print("Total acc = ", tacc, " index = ", idx)
        if tacc < minacc:
            minacc = tacc
            theindex = idx

   # print("minidx", theindex)

        # for i in range(10000):
        #     mindist = sys.maxsize
        #     best_idx = None
        #     for j in range(len(particles)):
        #         part = particles[j]
        #         part.vel += part.acc
        #         part.pos += part.vel
        #         part.dist = abs(part.pos.x) + abs(part.pos.y) + abs(part.pos.z)
        #         if(part.dist < mindist):
        #             mindist = part.dist
        #             best_idx = j
        #     if(i%100 == 0): print("Minimum distance (j = " ,best_idx, ":", mindist)

    print("Day 20 a = ", theindex)
    print("Day 20 b = ", 0)


if __name__ == "__main__":
    main()
