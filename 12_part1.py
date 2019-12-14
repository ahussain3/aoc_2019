from typing import NamedTuple
from collections import OrderedDict, defaultdict
import itertools
import pprint

moons = OrderedDict()
v_delta = defaultdict(lambda: {'x':0, 'y':0, 'z':0})

def run():
    for n1, n2 in itertools.product(moons.keys(), moons.keys()):
        if n1 == n2:
            continue

        m1 = moons[n1]
        m2 = moons[n2]

        for i in ['x', 'y', 'z']:
            if m1[i] > m2[i]:
                v_delta[n1][i] = v_delta[n1][i] - 0.5
                v_delta[n2][i] = v_delta[n2][i] + 0.5
            elif m1[i] < m2[i]:
                v_delta[n1][i] = v_delta[n1][i] + 0.5
                v_delta[n2][i] = v_delta[n2][i] - 0.5
            else:
                continue

    for n, m in moons.items():
        v = v_delta[n]
        for i in ['x', 'y', 'z']:
            m[i] = m[i] + v[i]

def energy():
    total = 0
    for n, m in moons.items():
        v = v_delta[n]
        u = abs(m['x']) + abs(m['y']) + abs(m['z'])
        k = abs(v['x']) + abs(v['y']) + abs(v['z'])
        total = total + (u * k)

    return total


def main():
    names = ['io', 'europa', 'ganymede', 'callisto']
    for line in open('12.in').readlines():
        x, y, z = map(lambda v: v.split("=")[1], line.strip("\n<>").split(", "))
        moons[names.pop(0)] = {'x':int(x),'y':int(y),'z':int(z)}

    for i in range(1000):
        print("timestep", i)
        pprint.pprint(moons)
        pprint.pprint(v_delta)
        run()

    print("energy", energy())
    return(energy)

main()
