#!/usr/bin/env python3

from collections import defaultdict
from itertools import combinations

def find_cliques(graph):
    cliques_of_size_3 = set()

    nodes = sorted(graph.keys())

    for triple in combinations(nodes, 3):
        if triple[0] in graph[triple[1]] and triple[0] in graph[triple[2]] and \
           triple[1] in graph[triple[2]]:
            cliques_of_size_3.add(tuple(sorted(triple)))

    return cliques_of_size_3

if __name__ == '__main__':
    with open('input') as fd:
        computers = set()
        connections = defaultdict(set)

        for line in fd:
            a, b = line.strip().split('-')
            connections[a].add(b)
            connections[b].add(a)

        cliques = find_cliques(connections)

        print([c for c in cliques if len(c) == 3])
        print({tuple(c) for c in cliques if len(c) == 3 and any(n.startswith('t') for n in c)})
        print(len({tuple(c) for c in cliques if len(c) == 3 and any(n.startswith('t') for n in c)}))
