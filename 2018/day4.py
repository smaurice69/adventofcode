
from itertools import count
from pathlib import Path
import sys
from collections import defaultdict
from utils.file_parsers import read_lines
from datetime import datetime, date, time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

class SleepInterval:
    def __init__(self, day: date, start: time, stop: time):
        self.day = day
        self.start = start
        self.stop = stop

    def duration_minutes(self):
        """Return total minutes asleep in this interval."""
        start_dt = datetime.combine(self.day, self.start)
        stop_dt  = datetime.combine(self.day, self.stop)
        return int((stop_dt - start_dt).total_seconds() // 60)

    def __repr__(self):
        return f"SleepInterval(day={self.day}, start={self.start}, stop={self.stop})"


class WorkerSleep:
    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self.intervals = []   # list of SleepInterval objects

    def add_sleep(self, day: date, start: time, stop: time):
        self.intervals.append(SleepInterval(day, start, stop))

    def total_sleep_minutes(self):
        return sum(interval.duration_minutes() for interval in self.intervals)

    def __repr__(self):
        return f"WorkerSleep(worker_id={self.worker_id}, intervals={self.intervals})"

def parse_date(date_str: str) -> datetime:
    """
    Parse a date string in the format: [YYYY-MM-DD HH:MM]
    Returns a datetime object.
    """
    # Strip the brackets
    cleaned = date_str.strip("[]")
    # Parse with datetime
    return datetime.strptime(cleaned, "%Y-%m-%d %H:%M")


def get_worker(workers, worker_id):
    if worker_id not in workers:
        workers[worker_id] = WorkerSleep(worker_id)
    return workers[worker_id]


def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day4test.txt')
    lines.sort()

    workers = {}

    for line in lines:
        sp = line.split(" ")
        thedate = parse_date(sp[0]+" "+sp[1])

        if sp[2]== "Guard":
            print(f"Guard {int(sp[3][1:])}")
            theworker = get_worker(workers, int(sp[3][1:]))
        elif sp[2]== "falls":
            print(f"falling asleep")
            starttime = thedate
        elif sp[2]== "wakes":
            print(f"wakeing asleep")
            stoptime = thedate
            theworker.add_sleep(starttime.date(), starttime.time(), stoptime.time())
        else:
            print("error")
            exit(1)

    print("Day 4 a =", 0)

    print("Day 4 b =", 0)
    
if __name__ == "__main__":
    main()
