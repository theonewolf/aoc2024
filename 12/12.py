#!/usr/bin/env python3

class NoNegativeIndexList(list):
    def __getitem__(self, index):
        if isinstance(index, int) and index < 0:
            raise IndexError("Negative indexing is not allowed.")
        return super().__getitem__(index)

def compute_perimeter(grid, x, y):
    rtype = grid[y][x]
    perimeter = 0

    try:
        if grid[y - 1][x] != rtype:
            print('Adding north perimeter')
            perimeter += 1
    except:
        print('Adding exception north perimeter')
        perimeter += 1

    try:
        if grid[y][x + 1] != rtype:
            print('Adding east perimeter')
            perimeter += 1
    except:
        print('Adding exception east perimeter')
        perimeter += 1

    try:
        if grid[y + 1][x] != rtype:
            print('Adding south perimeter')
            perimeter += 1
    except:
        print('Adding exception south perimeter')
        perimeter += 1

    try:
        if grid[y][x - 1] != rtype:
            print('Adding west perimeter')
            perimeter += 1
    except:
        print('Adding exception west perimeter')
        perimeter += 1

    print(f'{x,y} perimeter is {perimeter}')

    return perimeter

def walk_region(grid, rtype, x, y, region):
    print(f'[{x,y}] Working on {x,y}')
    if (x, y) in region:
        print(f'[{x,y}] Already in region, returning...')
        return region
    if y >= len(grid):
        print(f'[{x,y}] y is too high, returning')
        return region
    if x >= len(grid[0]):
        print(f'[{x,y}] x is too high, returning')
        return region

    if grid[y][x] != rtype:
        print(f'[{x,y}] Out of region, returning.')
        return region

    region |= {(x,y)}
    print(region)

    # Check north
    try:
        if grid[y - 1][x] == rtype:
            region |= walk_region(grid, rtype, x, y - 1, region)
    except:
        print(f'[{x,y}] Can not check north.')

    # Check east
    try:
        if grid[y][x + 1] == rtype:
            print(f'[{x,y}] Computing east region...')
            region |= walk_region(grid, rtype, x + 1, y, region)
            print(f'[{x,y}] Computed east...')
    except:
        print(f'[{x,y}] Can not check east.')

    print(region)

    # Check south
    try:
        if grid[y + 1][x] == rtype:
            print(f'[{x,y}] Computing south region...')
            region |= walk_region(grid, rtype, x, y + 1, region)
    except:
        print(f'[{x,y}] Can not check south.')

    # Check west
    try:
        if grid[y][x - 1] == rtype:
            print(f'[{x,y}] Computing west region...')
            region |= walk_region(grid, rtype, x - 1, y, region)
    except:
        print(f'[{x,y}] Can not check west.')

    print(f'[{x,y}] Returning final region: {region}')
    return region

def compute_region(grid, x, y):
    region = walk_region(grid, grid[y][x], x, y, set())
    perimeter = 0
    print(f'Region for {grid[y][x]} is {region}')
    for node in region:
        x, y = node
        perimeter += compute_perimeter(grid, x, y)

    return (grid[y][x], region, len(region), perimeter)

if __name__ == '__main__':
    with open('input') as fd:
        grid = NoNegativeIndexList([NoNegativeIndexList(list(c)) for c in [line.strip() for line in fd]])
        regions = []

        print(grid)

        visited = set()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                #if not (x == 6 and y == 0): continue
                if (x, y) in visited: continue
                regions.append(compute_region(grid, x, y))
                visited |= regions[-1][1]

        print(regions)
        print(sum([area * perimeter for _, _, area, perimeter in regions]))
