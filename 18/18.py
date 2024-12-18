#!/usr/bin/env python3

import heapq

MAX_EDGE = 71

# ChatGPT assist to remember this algorithm
def dijkstra(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    start, goal = (0, 0), (rows - 1, cols - 1)

    # Priority queue for Dijkstra (min-heap)
    pq = [(0, start)]  # (cost, (x, y))
    costs = {start: 0}  # Minimum cost to reach each position

    while pq:
        cost, (x, y) = heapq.heappop(pq)

        # If we've reached the goal, return the cost
        if (x, y) == goal:
            return cost

        # Process all neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the new position is within bounds and is not a wall
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '.':
                new_cost = cost + 1  # Each step has a cost of 1
                if (nx, ny) not in costs or new_cost < costs[(nx, ny)]:
                    costs[(nx, ny)] = new_cost
                    heapq.heappush(pq, (new_cost, (nx, ny)))

    # If the goal is unreachable
    return -1

def grid_str(grid):
    return '\n'.join([''.join(row) for row in grid])

if __name__ == '__main__':
    with open('input') as fd:
        grid = [['.' for _ in range(MAX_EDGE)] for _ in range(MAX_EDGE)]
        print(grid_str(grid))
        bytestack = []
        for line in fd:
            x,y = line.split(',')
            x,y = int(x),int(y)
            bytestack.append((x,y))

        count = 0
        for x,y in bytestack:
            grid[y][x] = '#'
            count += 1
            if count >= 1024: break

        print(grid_str(grid))
        print(bytestack)
        print(dijkstra(grid))
