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
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # North, East, South, West
    pq = [(0, start, FACING)]  # (cost, position)
    visited = set()
    distances = {start: 0}  # Cost to reach each position
    parents = {start: None}  # For reconstructing the path

    while pq:
        current_cost, current, facing = heapq.heappop(pq)
        if current in visited:
            continue

        visited.add(current)

        # If we reached the end, reconstruct and return the path
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return current_cost, path[::-1]  # Return reversed path

        # Explore neighbors
        for dx, dy in directions:
            if facing == (dx, dy):
                cost = 1
            elif dx == 0 and facing[0] != 0:
                cost = 1001
            elif dy == 0 and facing [1] !=0:
                cost = 1001
            else:
                cost = 2002
            nx, ny = current[0] + dx, current[1] + dy
            next_pos = (nx, ny)

            if 0 <= nx < rows and 0 <= ny < cols and maze[ny][nx] != WALL: # Valid and not a wall
                new_cost = current_cost + cost
                if next_pos not in distances or new_cost < distances[next_pos]:
                    distances[next_pos] = new_cost
                    heapq.heappush(pq, (new_cost, next_pos, (dx, dy)))
                    parents[next_pos] = current
    print(visited)

    return None  # No path found

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
