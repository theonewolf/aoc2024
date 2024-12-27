#!/usr/bin/env python3

from collections import defaultdict
from itertools import combinations

import networkx as nx

def find_cliques2(graph):
    G = nx.Graph()
    G.add_edges_from([(k, n) for k,v in graph.items() for n in v])

    cliques = nx.find_cliques(G)
    return max(cliques, key=len)

if __name__ == '__main__':
    with open('input') as fd:
        computers = set()
        connections = defaultdict(set)

        for line in fd:
            a, b = line.strip().split('-')
            connections[a].add(b)
            connections[b].add(a)

        maxclique = find_cliques2(connections)

        print(','.join(sorted(maxclique)))
