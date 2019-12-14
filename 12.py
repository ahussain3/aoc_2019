from typing import NamedTuple
from collections import OrderedDict, defaultdict
import itertools
import pprint

orig_moons = OrderedDict()
orig_v_delta = defaultdict(lambda: {'x':0.0, 'y':0.0, 'z':0.0})

moons = OrderedDict()
v_delta = defaultdict(lambda: {'x':0.0, 'y':0.0, 'z':0.0})

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
    for i, line in enumerate(open('12.in').readlines()):
        x, y, z = map(lambda v: v.split("=")[1], line.strip("\n<>").split(", "))
        moons[names[i]] = {'x':float(x),'y':float(y),'z':float(z)}
        orig_moons[names[i]] = {'x':float(x),'y':float(y),'z':float(z)}
        orig_v_delta[names[i]] = {'x':0.0,'y':0.0,'z':0.0}

    run()

    i = 0
    while True:
        i = i + 1
        if i % 100000 == 0:
            print("timestep", i)
        if moons == orig_moons and v_delta == orig_v_delta:
            print("timestep", i)
            break
        run()

    print("energy", energy())
    return(energy)

main()
