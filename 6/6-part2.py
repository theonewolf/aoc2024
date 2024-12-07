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
                    return (i, j, grid[i][j])
                else:
                    grid[i][j] = CLEAR
                    i += move_y
                    j += move_x
                    grid[i][j] = column
                    return (i, j, grid[i][j])

# Place obstacles on the map, if we return to start we count a loop
def reset_grid(grid):
    newgrid = NoNegativeIndexList(grid)
    for i, row in enumerate(newgrid):
        newgrid[i] = NoNegativeIndexList(row)
    return newgrid

def start(grid):
    for i, row in enumerate(grid):
        for j, column in enumerate(row):
            if column == UP:
                return (i,j)

if __name__ == '__main__':
    with open('input') as fd:
        loops = 0
        grid = fd.read().split()
        newgrid = reset_grid(grid)
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                newgrid = reset_grid(grid)
                
                print(f'Testing obstacle at (x={j},y={i})')
                if newgrid[i][j] == CLEAR:
                    newgrid[i][j] = OBSTACLE

                y,x = start(newgrid)
                steps = set((y,x,UP))

                while True:
                    try:
                        nextstep = step(newgrid)
                        if nextstep in steps:
                            print('Loop detected')
                            loops += 1
                            break
                        steps.add(nextstep)
                    except:
                        print('Escaped...')
                        break

        print(loops)
