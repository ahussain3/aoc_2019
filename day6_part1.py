from typing import Optional

nodes = {}

def count_indirect_orbits(name):
    count = 1
    while nodes[name] != 'COM':
        count = count + 1
        name = nodes[name]
    return count

def run():
    with open("day6_input.txt", 'r') as f:
        for line in f.readlines():
            root, orbiter = line.strip().split(")")
            nodes[orbiter] = root

    # import pprint
    # pprint.pprint(nodes)
    # print("D orbits", count_indirect_orbits('D'))

    result = sum(count_indirect_orbits(name) for name in nodes.keys())
    print("Number of indirect orbits:", result)


if __name__ == "__main__":
    run()