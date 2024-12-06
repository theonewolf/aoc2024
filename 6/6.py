#!/usr/bin/env python3

from pprint import pprint

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'
OBSTACLE = '#'
CLEAR = '.'
# x,y movement
TURNMOV = {UP : (0, -1), DOWN : (0, 1), LEFT : (-1, 0), RIGHT : (1, 0)}
TURNMAP = {UP : RIGHT, DOWN : LEFT, LEFT : UP, RIGHT : DOWN}
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}

class NoNegativeIndexList(list):
    def __getitem__(self, index):
        if isinstance(index, int) and index < 0:
            raise IndexError("Negative indexing is not allowed.")
        return super().__getitem__(index)

def step(grid):
    for i, row in enumerate(grid):
        for j, column in enumerate(row):
            if column in DIRECTIONS:
                move_x, move_y = TURNMOV[column]
                if grid[i + move_y][j + move_x] == OBSTACLE:
                    grid[i][j] = TURNMAP[column]
                    return (i, j)
                else:
                    grid[i][j] = CLEAR
                    grid[i + move_y][j + move_x] = column
                    return (i + move_y, j + move_x)

if __name__ == '__main__':
    with open('input') as fd:
        grid = fd.read().split()
        newgrid = NoNegativeIndexList(grid)
        for i, row in enumerate(newgrid):
            newgrid[i] = NoNegativeIndexList(row)

        steps = set()
        while True:
            try:
                steps.add(step(newgrid))
            except:
                break

        # This can be off by one, need to account for starting position.
        print(len(steps))
