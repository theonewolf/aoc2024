#!/usr/bin/env python3

# a good hiking trail is as long as possible and has an even, gradual, uphill
# slope. For all practical purposes, this means that a hiking trail is any path
# that starts at height 0, ends at height 9, and always increases by a height
# of exactly 1 at each step. Hiking trails never include diagonal steps - only
# up, down, left, or right (from the perspective of the map).

# A trailhead is any position that starts one or more hiking trails - here,
# these positions will always have height 0. Assembling more fragments of
# pages, you establish that a trailhead's score is the number of 9-height
# positions reachable from that trailhead via a hiking trail.

TRAILHEAD = 0
TRAILTAIL = 9

class NoNegativeIndexList(list):
    def __getitem__(self, index):
        if isinstance(index, int) and index < 0:
            raise IndexError("Negative indexing is not allowed.")
        return super().__getitem__(index)

def find_all_trails(grid, x, y):
    current = grid[y][x]
    nextval = current + 1
    north = 0
    east = 0
    south = 0
    west = 0
    ntails = set()
    etails = set()
    stails = set()
    wtails = set()

    if current == TRAILTAIL: return (1, {(x, y)})

    # North
    try:
        if grid[y - 1][x] == nextval:
            north, ntails = find_all_trails(grid, x, y - 1)
    except:
        print('Can not go North.')

    # East
    try:
        if grid[y][x + 1] == nextval:
            east, etails = find_all_trails(grid, x + 1, y)
    except:
        print('Can not go East.')

    # South
    try:
        if grid[y + 1][x] == nextval:
            west, wtails = find_all_trails(grid, x, y + 1)
    except:
        print('Can not go South.')

    # West
    try:
        if grid[y][x - 1] == nextval:
            south, stails = find_all_trails(grid, x - 1, y)
    except:
        print('Can not go West.')

    return north + east + south + west, ntails | etails | stails | wtails

if __name__ == '__main__':
    with open('input') as fd:
        grid = NoNegativeIndexList([NoNegativeIndexList([int(c) if c.isdigit() else c for c in line.strip()]) for line in fd])
        tails = set()
        trails = []
        tail_counts = []
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                if col == TRAILHEAD:
                    print(f'Found trailhead at {x},{y}')
                    trail_count, reachable_tails = find_all_trails(grid, x, y)
                    print(reachable_tails)
                    tails |= reachable_tails
                    tail_counts += [len(reachable_tails)]
                    trails += [trail_count]
        print(tails)
        print(len(tails))
        print(sum(tail_counts))
        print('-------')
        print(trails)
        print(sum(trails))
