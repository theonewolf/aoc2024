#!/usr/bin/env python3

# The lanternfish use their own custom Goods Positioning System (GPS for short)
# to track the locations of the boxes. The GPS coordinate of a box is equal to
# 100 times its distance from the top edge of the map plus its distance from
# the left edge of the map. (This process does not stop at wall tiles; measure
# all the way to the edges of the map.)

def gridstr(grid):
    return '\n'.join([''.join(row) for row in grid])

def find_robot(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == '@': return (x, y)
    raise Exception('OMG can not find robot...')

# As the robot (@) attempts to move, if there are any boxes (O) in the way, the
# robot will also attempt to push those boxes. However, if this action would
# cause the robot or a box to move into a wall (#), nothing moves instead,
# including the robot. The initial positions of these are shown on the map at
# the top of the document the lanternfish gave you.
def step(grid, robot_x, robot_y, instruction):
    # Setup direction
    match instruction:
        case '<':
            dist = robot_x
            dx = -1
            dy = 0
        case '>':
            dist = len(grid[0]) - robot_x
            dx = 1
            dy = 0
        case '^':
            dist = robot_y
            dy = -1
            dx = 0
        case 'v':
            dist = len(grid) - robot_y
            dy = 1
            dx = 0
        case _:
            raise Exception("Unknown direction")

    # Check if clear
    clear = False
    start_x = None
    start_y = None
    for i in range(1, dist + 1):
        if grid[robot_y + i * dy][robot_x + i * dx] == '#':
            print('Not clear...')
            break
        elif grid[robot_y + i * dy][robot_x + i * dx] == '.':
            print('Clear!')
            dist = i
            clear = True
            start_x = robot_x + i * dx
            start_y = robot_y + i * dy
            break

    if clear:
        print(f'Distance to move things: {dist}')

        # need to move things backwards
        for i in range(dist):
            grid[start_y - i * dy][start_x - i * dx] = grid[start_y - (i + 1) * dy][start_x - (i + 1) * dx]
            if grid[start_y - (i + 1) * dy][start_x - (i + 1) * dx] == '@':
                grid[start_y - (i + 1) * dy][start_x - (i + 1) * dx] = '.'
                robot_x = start_x - i * dx
                robot_y = start_y - i * dy

    return (robot_x, robot_y)
    
def gps(grid):
    score = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 'O':
                score += y * 100 + x
    return score

if __name__ == '__main__':
    with open('input') as fd:
        grid = []
        instructions = []
        for line in fd:
            line = line.strip()
            if '#' in line:
                grid.append([c for c in line])
            elif line:
                instructions.append(line)

        robot_x, robot_y = find_robot(grid)
        instructions = ''.join(instructions)

        for i in instructions:
            print(f'--- Move: {i} -----------------------------')
            robot_x, robot_y = step(grid, robot_x, robot_y, i)
            print(f'Robot at: ({robot_x}, {robot_y})')
            print(gridstr(grid))

        print(gridstr(grid))
        print(instructions)

        print(gps(grid))
