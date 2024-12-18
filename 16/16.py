#!/usr/bin/env python3

import heapq

WALL = '#'
EMPTY = '.'
START = 'S'
END = 'E'
FACING = (1,0)

# ChatGPT helped ideate on how to approach.  I picked Dijkstra and modified
# the cost values.  It was tricky to determine 1001, but you have to realize
# that to make the move requires a 90-degree turn and a step.
def dijkstra(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # North, East, South, West
    turns = {(0, -1): [(1, 0), (-1, 0)],
             (1, 0): [(0, -1), (0, 1)],
             (0, 1): [(1, 0), (-1, 0)],
             (-1, 0): [(0, 1), (0, -1)]}
    pq = [(0, start, FACING)]  # (cost, position)
    visited = set()
    distances = {start: 0}  # Cost to reach each position
    parents = {start: None}  # For reconstructing the path

    while pq:
        current_cost, current, facing = heapq.heappop(pq)

        # If we reached the end, reconstruct and return the path
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return current_cost, path[::-1]  # Return reversed path

        if (current, facing) in visited:
            continue

        visited.add((current, facing))

        # Explore neighbors
        for dx, dy in directions:
            if facing == (dx, dy):
                cost = 1
            elif (dx, dy) in turns[facing]:
                cost = 1001
            else:
                continue
            nx, ny = current[0] + dx, current[1] + dy
            next_pos = (nx, ny)

            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] != WALL: # Valid and not a wall
                new_cost = current_cost + cost
                if next_pos not in distances or new_cost < distances[next_pos]:
                    distances[next_pos] = new_cost
                    heapq.heappush(pq, (new_cost, next_pos, (dx, dy)))
                    parents[next_pos] = current
    print(visited)

    return None  # No path found


def dijkstra_with_turns_all_paths(grid, start, end, start_direction='RIGHT'):
    rows, cols = len(grid), len(grid[0])
    directions = {
        'UP': (0, -1),     # Move up: decrease y
        'DOWN': (0, 1),    # Move down: increase y
        'LEFT': (-1, 0),   # Move left: decrease x
        'RIGHT': (1, 0)    # Move right: increase x
    }
    turns = {
        'UP': ['LEFT', 'RIGHT'],
        'DOWN': ['LEFT', 'RIGHT'],
        'LEFT': ['UP', 'DOWN'],
        'RIGHT': ['UP', 'DOWN']
    }

    # Priority queue: (cost, x, y, direction, path)
    pq = [(0, start[0], start[1], start_direction, [(start[0], start[1])])]  # Path starts with the initial position
    best_cost = float('inf')
    best_paths = []
    visited = {}

    while pq:
        cost, x, y, direction, path = heapq.heappop(pq)

        # If we've exceeded the best cost, stop exploring
        if cost > best_cost:
            continue

        # Stop when reaching the end
        if (x, y) == end:
            if cost < best_cost:
                best_cost = cost
                best_paths = [path]
            elif cost == best_cost:
                best_paths.append(path)
            continue

        # Avoid revisiting the same cell with the same direction at a higher cost
        if (x, y, direction) in visited and visited[(x, y, direction)] <= cost:
            continue
        visited[(x, y, direction)] = cost

        # Move straight
        dx, dy = directions[direction]
        nx, ny = x + dx, y + dy
        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] != WALL:  # Check bounds and passable cell
            heapq.heappush(pq, (cost + 1, nx, ny, direction, path + [(nx, ny)]))

        # Turn left and right (90-degree turn costs 1000)
        for new_direction in turns[direction]:
            heapq.heappush(pq, (cost + 1000, x, y, new_direction, path))

    return best_cost, best_paths

def dijkstra_with_turns(grid, start, end, start_direction='RIGHT'):
    rows, cols = len(grid), len(grid[0])  # Grid dimensions
    directions = {
        'UP': (0, -1),     # Move up: decrease y
        'DOWN': (0, 1),    # Move down: increase y
        'LEFT': (-1, 0),   # Move left: decrease x
        'RIGHT': (1, 0)    # Move right: increase x
    }
    turns = {
        'UP': ['LEFT', 'RIGHT'],
        'DOWN': ['LEFT', 'RIGHT'],
        'LEFT': ['UP', 'DOWN'],
        'RIGHT': ['UP', 'DOWN']
    }

    # Priority queue: (cost, x, y, direction)
    pq = [(0, start[0], start[1], start_direction)]  # Start facing the given direction
    visited = set()

    while pq:
        cost, x, y, direction = heapq.heappop(pq)

        # Stop when reaching the end
        if (x, y) == end:
            return cost

        # Avoid revisiting the same cell with the same direction
        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))

        # Move straight
        dx, dy = directions[direction]
        nx, ny = x + dx, y + dy
        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] != WALL:  # Check bounds and passable cell
            heapq.heappush(pq, (cost + 1, nx, ny, direction))

        # Turn left and right (90-degree turn costs 1000)
        for new_direction in turns[direction]:
            heapq.heappush(pq, (cost + 1000, x, y, new_direction))

    return -1  # No path found

def find_start(maze):
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if col == 'S':
                return (j,i)

    raise Exception('THERE IS NO START.')

def find_end(maze):
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if col == 'E':
                return (j,i)

    raise Exception('THERE IS NO END.')

if __name__ == '__main__':
    with open('input') as fd:
        maze = fd.read().split()
        start = find_start(maze)
        end = find_end(maze)

        print(f'start={start}, end={end}')
        print('\n'.join(maze))
        print(dijkstra(maze, start, end))
        print(dijkstra_with_turns(maze, start, end))
        cost, paths = dijkstra_with_turns_all_paths(maze, start, end)
        print(cost)
        print(set([step for path in paths for step in path]))
        print(len(set([step for path in paths for step in path])) + 1 + 1)
