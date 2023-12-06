import sys
import re
import numpy as np

from scipy.optimize import linprog
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

for s in sensors:
    print(s.describe())
    print(s.radius)


def inequality_coefficients(i, j, r):
    coef_x_1, coef_y_1, c_1 = -1, -1, -i - j - r
    coef_x_2, coef_y_2, c_2 = -1, 1, -i + j - r
    coef_x_3, coef_y_3, c_3 = -1, 1, i - j - r
    coef_x_4, coef_y_4, c_4 = -1, -1, i + j -r

    return np.array([
        [coef_x_1, coef_y_1],
        [coef_x_2, coef_y_2],
        [coef_x_3, coef_y_3],
        [coef_x_4, coef_y_4]
        ]), np.array([c_1, c_2, c_3, c_4]).T

# Parameters
MAX_COORD = 4000000

c = [1, 1]

A, b = [], []
for s in sensors:
    A_s, b_s = inequality_coefficients(s.sx, s.sy, s.radius)
    A.append(A_s)
    b.append(b_s)

A = np.concatenate(A)
b = np.concatenate(b)

res = linprog(c, A_ub = A, b_ub = b, bounds = np.array([[0, MAX_COORD], [0, MAX_COORD]]))

print(res)

#print(field)
#argmin = np.argmin(field)
#argx = argmin // MAX_COORD
#argy = argmin % MAX_COORD
#print(f'x = {argx}, y = {argy}')
