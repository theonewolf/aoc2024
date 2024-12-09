#!/usr/bin/env python3

import sys

from math import atan2, cos, degrees, sin, sqrt
from pprint import pprint

# In particular, an antinode occurs at any point that is perfectly in line with
# two antennas of the same frequency - but only when one of the antennas is twice
# as far away as the other.

ANTINODE = '#'
EMPTY = '.'

class NoNegativeIndexList(list):
    def __getitem__(self, index):
        if isinstance(index, int) and index < 0:
            raise IndexError("Negative indexing is not allowed.")
        return super().__getitem__(index)

    def __str__(self):
        rep = ''
        for row in self:
            rep += ''.join(row)
            rep += '\n'
        return rep

def unique_frequencies(grid):
    freqs = set()

    for row in grid:
        for col in row:
            if col != EMPTY:
                freqs.add(col)
    return freqs

def antenna_locations(grid, freqs):
    locations = {f : [] for f in freqs}

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col != EMPTY:
                locations[col] += [(j,i)]
    return locations

def compute_delta(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    dy = y1 - y2
    dx = x1 - x2

    return (dx, dy)

def compute_antinodes(points, max_x, max_y):
    antinodes = set()

    for p1 in points:
        for p2 in points:
            if p1 == p2: continue
            x, y = p1
            step_x, step_y = compute_delta(p1, p2)

            while (x < max_x and y < max_y) and not (x < 0 or y < 0):
                print(f'Line between {p1} <-> {p2} delta is ({step_x}, {step_y}) new position {(x, y)}.')
                antinodes.add((x, y))
                x, y = x + step_x, y + step_y

    return antinodes

if __name__ == '__main__':
    with open('input') as fd:
        grid = fd.read().split()
        newgrid = NoNegativeIndexList(grid)
        max_y = len(newgrid)
        max_x = sys.maxsize
        for i, row in enumerate(newgrid):
            newgrid[i] = NoNegativeIndexList(row)
            max_x = min(max_x, len(newgrid[i]))

        freqs = unique_frequencies(newgrid)
        locations = antenna_locations(grid, freqs)
        pprint(newgrid)
        pprint(freqs)
        pprint(locations)
        antinodes = set()
        for freq in freqs:
            antinodes |= compute_antinodes(locations[freq], max_x, max_y)

        for x,y in antinodes:
            if newgrid[y][x] == EMPTY:
                newgrid[y][x] = ANTINODE
        pprint(antinodes)
        print(newgrid)
        print(len(antinodes))
