import sys
import re
import numpy as np

from tqdm import tqdm

def manhattan(a, b):
    return np.sum(np.abs(a - b))

class Sensor:
    def __init__(self, sx, sy, bx, by):
        self.sx = int(sx)
        self.sy = int(sy)
        self.bx = int(bx)
        self.by = int(by)


    def __repr__(self):
        return f"Sensor({self.sx},{self.sy})"

    def describe(self):
        return f"Sensor at ({self.sx},{self.sy}) detects Beacon at ({self.bx},{self.by})"

    @property
    def position(self):
        return np.array([self.sx, self.sy])

    @property
    def x(self):
        return self.sx

    @property
    def y(self):
        return self.sy

    @property
    def beacon(self):
        return np.array([self.bx, self.by])

    @property
    def radius(self):
        return manhattan(self.position, self.beacon)

    def doesnt_have_beacon(self, other_position):
        return manhattan(self.position, other_position) <= self.radius

    @classmethod
    def Factory(cls, line):
        line = line.strip()
        sensor_regex = "Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)"

        match = re.match(sensor_regex, line)
        sx, sy, bx, by = match[1], match[2], match[3], match[4]
        return cls(sx, sy, bx, by)

beacons = []
sensors = []

with open(sys.argv[1],'r') as f:
    for line in f:
        s = Sensor.Factory(line)
        beacons.append(tuple(s.beacon))
        sensors.append(s)
beacons = set(beacons)

# Parameters
# y = 2000000
y = 10

close_sensors = [s for s in sensors if np.abs(s.position[1] - y) < s.radius]

print(len(close_sensors))

safe_positions = set()
for s in close_sensors:
    s.describe()
    min_x = s.x - s.radius + np.abs(s.y - y) - 1
    max_x = s.x + s.radius - np.abs(s.y - y) + 1
    for x in tqdm(range(min_x, max_x)):
        if x in safe_positions:
            continue

        if s.doesnt_have_beacon(np.array([x,y])):
            safe_positions.add(x)

for b in beacons:
    if b[1] == y and (b[0] in safe_positions):
        safe_positions.remove(b[0])

n_safe = len(safe_positions)
print(n_safe)
