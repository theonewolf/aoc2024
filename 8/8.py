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
                locations[col] += [(i,j)]
    return locations

def euclidean_distance(p1, p2):
    y1, x1 = p1
    y2, x2 = p2
    return round(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

def compute_angle(p1, p2):
    y1,x1 = p1
    y2,x2 = p2
    return atan2(y1 - y2, x2 - x1)

def new_position(p, distance, angle):
    y, x = p
    # Calculate new point based on angle and distance
    x_new = x + distance * cos(angle)
    y_new = y - distance * sin(angle)
    return (round(x_new), round(y_new))

def compute_antinodes(points, max_x, max_y):
    antinodes = set()
    for p1 in points:
        for p2 in points:
            if p1 == p2: continue
            angle = compute_angle(p1, p2)
            distance = euclidean_distance(p1, p2)
            antinode_x, antinode_y = new_position(p2, distance, angle)
            if antinode_x < 0 or antinode_y < 0: continue
            if antinode_x >= max_x or antinode_y >= max_y: continue
            antinodes.add((antinode_x, antinode_y))
            print(f'Line between {p1} <-> {p2} distance {distance}, angle {degrees(angle)}, new position {(antinode_x, antinode_y)}.')
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
