from typing import Optional

nodes = {}

def count_indirect_orbits(name):
    count = 1
    while nodes[name] != 'COM':
        count = count + 1
        name = nodes[name]
    return count

def path_from_node(name):
    path = []
    while nodes[name] != 'COM':
        name = nodes[name]
        path.append(name)
    return path

def shortest_path_intersection(patha, pathb):
    intersections = set(patha).intersection(set(pathb))
    print(intersections)
    min_dist = 9999999999999
    for i in intersections:
        dist = patha.index(i) + pathb.index(i)
        if dist < min_dist:
            min_dist = dist
    return min_dist

def run():
    with open("day6_input.txt", 'r') as f:
        for line in f.readlines():
            root, orbiter = line.strip().split(")")
            nodes[orbiter] = root

    # import pprint
    # pprint.pprint(nodes)

    path_you = path_from_node('YOU')
    path_san = path_from_node('SAN')
    print("YOU path", path_you)
    print("SAN path", path_san)

    shortest_path_length = shortest_path_intersection(path_you, path_san)
    print("Shortest path length", shortest_path_length)

if __name__ == "__main__":
    run()