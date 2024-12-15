#!/usr/bin/env python3

from collections import Counter

class Robot:
    def __init__(self, x=0, y=0, vx=0, vy=0, bound_x=101, bound_y=103):
        """
        Initialize the Robot with position (x, y) and velocity (vx, vy).
        Defaults to (0, 0) for position and (0, 0) for velocity.
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.bound_x = bound_x
        self.bound_y = bound_y

    @classmethod
    def from_string(cls, data, bound_x=101, bound_y=103):
        """
        Initializes a Robot instance from a string formatted as 'p=x,y v=vx,vy'.
        Example: 'p=0,4 v=3,-3'
        """
        try:
            position_part, velocity_part = data.split(" ")
            px, py = map(int, position_part[2:].split(","))
            vx, vy = map(int, velocity_part[2:].split(","))
            return cls(px, py, vx, vy, bound_x, bound_y)
        except (ValueError, IndexError):
            raise ValueError("Input string must be formatted as 'p=x,y v=vx,vy'")

    def move(self):
        """
        Updates the Robot's position based on its velocity.
        """
        self.x += self.vx

        if self.x < 0:
            self.x += self.bound_x
        
        self.y += self.vy

        if self.y < 0:
            self.y += self.bound_y

        self.x %= self.bound_x
        self.y %= self.bound_y

    def grid(self):
        grid = [['.' for _ in range(self.bound_x)] for _ in range(self.bound_y)]
        grid[self.y][self.x] = 'R'
        return '\n'.join([''.join(row) for row in grid])

    @classmethod
    def plot_robots(cls, robots, bound_x=101, bound_y=103):
        grid = [['.' for _ in range(bound_x)] for _ in range(bound_y)]
        for robot in robots:
            x,y = robot.x, robot.y
            grid[y][x] = 'R'
        return '\n'.join([''.join(row) for row in grid])

    @classmethod
    # Note: ChatGPT let me iterate ideas REALLY quickly -- Wolf
    def likely_christmas_tree(cls, robots):
        # Extract robot positions as a set of (x, y) tuples
        robot_positions = {(robot.x, robot.y) for robot in robots}

        # Find bounds of the grid based on robot positions
        if not robot_positions:
            return []

        min_x = min(x for x, y in robot_positions)
        max_x = max(x for x, y in robot_positions)
        min_y = min(y for x, y in robot_positions)
        max_y = max(y for x, y in robot_positions)

        clusters = []

        # Iterate over possible top-left corners of 4x4 clusters
        for x in range(min_x, max_x - 3 + 1):  # +1 to include the right boundary
            for y in range(min_y, max_y - 3 + 1):  # +1 to include the bottom boundary
                # Check if all positions in this 4x4 grid are occupied
                is_cluster = all(
                    (x + dx, y + dy) in robot_positions
                    for dx in range(4)
                    for dy in range(4)
                )
                if is_cluster:
                    clusters.append((x, y))  # Store the top-left corner of the cluster
        return len(clusters) > 0


    def quadrant(self):
        q1 = self.x < self.bound_x // 2 and self.y < self.bound_y // 2
        q2 = self.x > self.bound_x // 2 and self.y < self.bound_y // 2
        q3 = self.x > self.bound_x // 2 and self.y > self.bound_y // 2
        q4 = self.x < self.bound_x // 2 and self.y > self.bound_y // 2

        if q1: return 1
        if q2: return 2
        if q3: return 3
        if q4: return 4

        print(f'Robot not inside a quadrant: {self}')
        return 0

    def __repr__(self):
        """
        String representation of the Robot.
        """
        return f"Robot(Position: ({self.x}, {self.y}), Velocity: ({self.vx}, {self.vy}, Bounds: ({self.bound_x}, {self.bound_y})))"

if __name__ == '__main__':
    with open('input') as fd:
        robots = [Robot.from_string(line) for line in fd]

        seconds = 0
        while not Robot.likely_christmas_tree(robots):
            for robot in robots: robot.move()
            seconds += 1
            if not seconds % 100: print(f'Current second: {seconds}')

        quadrants = [robot.quadrant() for robot in robots]
        quadrants = [quadrants.count(i) for i in range(5)]

        print(quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4])

        print(Robot.plot_robots(robots))
        print(f'Found Christmas Tree in {seconds}')
