import itertools
from collections import defaultdict
from typing import NamedTuple, Tuple
from math import pi, atan2, sqrt

data = []
o = origin = (31, 20)
asteroids = []

class Asteroid(NamedTuple):
    p: Tuple[int,int]
    angle: float
    distance: float

    def __repr__(self):
        return f"({self.p[0]},{self.p[1]})"

def print_asteroids(input, marker=None):
    print(" ", " ".join(str(i).rjust(2) for i in range(len(input[0]))))
    for j in range(len(input)):
        print(str(j).ljust(2), end=" ")
        for i in range(len(input[0])):
            if (i, j) == marker:
                val = "*"
            elif (i, j) in data:
                val = "#"
            else:
                val = "."
            print(val, end="  ")
        print("")

def get_angle(p, o):
    x = p[0] - o[0]
    y = o[1] - p[1]
    angle = atan2(-y, x)

    if angle < 0: angle = (2*pi) + angle  # map to 0-360
    angle = angle + pi / 2  # rotate by 90 deg
    if angle >= 2*pi: angle = angle - 2*pi # renormalize
    return angle

def get_distance(p, o):
    x = p[0] - o[0]
    y = p[1] - o[1]
    return sqrt(x ** 2 + y ** 2)

def main():
    input = open('10.in').read().split("\n")
    for col, line in enumerate(input):
        for row, point in enumerate(line):
            if input[col][row] == "#":
                data.append((row,col))

    # for i in [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1),(0,1)]:
    #     print(i, get_angle(i, (0,0)) / pi)

    for a in data:
        asteroids.append(Asteroid(a, get_angle(a, o), get_distance(a, o)))

    asteroids.sort(key=lambda a: (a.angle, a.distance))

    def shove_duplicates(asteroids):
        result = [asteroids[0]]
        dupes = []
        for a1, a2 in zip(asteroids, asteroids[1:]):
            if a2.angle == a1.angle:
                # we have a duplicate
                dupes.append(a2)
            else:
                result.append(a2)
        result.extend(dupes)
        return result, dupes

    result, dupes = shove_duplicates(asteroids)

    while dupes:
        result, dupes = shove_duplicates(result)

    return result[199]

# Approach:
# For each asteroid, calculate its angle and distance.
# sort by angle and then distance
# take any duplicated angles and move them to the back of the queue, repeat.

main()
