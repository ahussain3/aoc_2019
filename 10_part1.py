import itertools
from collections import defaultdict

asteroids = []
can_see = defaultdict(set)

def print_asteroids(input):
    for j in range(len(input)):
        for i in range(len(input[0])):
            val = "#" if (i,j) in asteroids else "."
            print(val, end="")
        print("")

def get_liminal_points(a, b):
    liminal_points = []

    if a[0] == b[0]:
        # horizontal line
        return [(a[0], i) for i in range(min(a[1], b[1])+1, max(a[1],b[1]))]

    if a[1] == b[1]:
        # vertical line
        return [(i, a[1]) for i in range(min(a[0], b[0])+1, max(a[0],b[0]))]

    if a[0] > b[0]:
        a, b = b, a

    m = (b[1] - a[1]) / (b[0] - a[0])
    for x in range(a[0] + 1, b[0]):
        y = m * (x - a[0]) + a[1]
        if y.is_integer():
            liminal_points.append((x, int(y)))

    return liminal_points

def print_hits(input, a):
    for j in range(len(input)):
        for i in range(len(input[0])):
            if (i, j) == a:
                val = "*"
            elif (i, j) in can_see[a]:
                val = "1"
            elif (i, j) in asteroids:
                val = "#"
            else:
                val = "."
            print(val, end=" ")
        print("\n")

def main():
    input = open('10.in').read().split("\n")
    for col, line in enumerate(input):
        for row, point in enumerate(line):
            if input[col][row] == "#":
                asteroids.append((row,col))

    for a, b in itertools.product(asteroids, repeat=2):
        if a == b:
            continue

        liminal_points = get_liminal_points(a, b)

        if all(p not in asteroids for p in liminal_points):
            can_see[a].add(b)
            can_see[b].add(a)

    print(asteroids)
    print_asteroids(input)

    for a, hits in can_see.items():
        print(a, len(hits))

    print(max(*[len(hits) for _, hits in can_see.items()]))

# Two possible approaches:
# 1) For each asteroid fan out and see what you hit
    # Something with greatest common multiples etc? Sieve of erastothanes style?
# 2) For each asteroid, compare it to every other one and see if they can see each other.
    # how to detect what is on the line between them?
# let me try approach 2. I think I can detect all integer points between two points?

main()
