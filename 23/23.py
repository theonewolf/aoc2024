#!/usr/bin/env python3

from collections import defaultdict
from itertools import combinations

def is_clique(graph, nodes):
    return all(node2 in graph[node1] for node1 in nodes for node2 in nodes if node1 != node2)

def bron_kerbosch(R, P, X, graph, cliques):
    if not P and not X:
        cliques.append(sorted(R))  # Canonicalize order
    for v in sorted(P):  # Sorted to ensure consistent processing order
        bron_kerbosch(
            R | {v}, P & graph[v], X & graph[v], graph, cliques
        )
        P.remove(v)
        X.add(v)

def find_all_subcliques(graph, cliques, size):
    smaller_cliques = []
    for clique in cliques:
        if len(clique) >= size:
            for subset in combinations(sorted(clique), size):
                if is_clique(graph, subset):
                    smaller_cliques.append(set(subset))
    return sorted(map(sorted, smaller_cliques))  # Deduplicate and sort

if __name__ == '__main__':
    with open('input') as fd:
        computers = set()
        connections = defaultdict(set)

        for line in fd:
            a, b = line.strip().split('-')
            connections[a].add(b)
            connections[b].add(a)

        print(connections)
        cliques = []
        bron_kerbosch(set(), set(connections.keys()), set(), connections, cliques)

        smaller_cliques = find_all_subcliques(connections, cliques, 3)

        cliques += smaller_cliques

        print([c for c in cliques if len(c) == 3])
        print({tuple(c) for c in cliques if len(c) == 3 and any('t' in n for n in c)})
        print(len({tuple(c) for c in cliques if len(c) == 3 and any('t' in n for n in c)}))
