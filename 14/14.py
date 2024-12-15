#!/usr/bin/env python3

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
    def from_string(cls, data):
        """
        Initializes a Robot instance from a string formatted as 'p=x,y v=vx,vy'.
        Example: 'p=0,4 v=3,-3'
        """
        try:
            position_part, velocity_part = data.split(" ")
            px, py = map(int, position_part[2:].split(","))
            vx, vy = map(int, velocity_part[2:].split(","))
            return cls(px, py, vx, vy)
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

    def set_velocity(self, vx, vy):
        """
        Sets the Robot's velocity to (vx, vy).
        """
        self.vx = vx
        self.vy = vy

    def get_position(self):
        """
        Returns the current position of the Robot as a tuple (x, y).
        """
        return (self.x, self.y)

    def get_velocity(self):
        """
        Returns the current velocity of the Robot as a tuple (vx, vy).
        """
        return (self.vx, self.vy)

    def grid(self):
        grid = [['.' for _ in range(self.bound_x)] for _ in range(self.bound_y)]
        grid[self.y][self.x] = 'R'
        return '\n'.join([''.join(row) for row in grid])

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
        return f"Robot(Position: ({self.x}, {self.y}), Velocity: ({self.vx}, {self.vy}))"

if __name__ == '__main__':
    with open('input') as fd:
        robots = []
        for line in fd:
           robots.append(Robot.from_string(line))
           #robots[-1].bound_x = 11
           #robots[-1].bound_y = 7

        for i in range(100):
            for robot in robots:
                robot.move()

        quadrants = [robot.quadrant() for robot in robots]
        q1 = quadrants.count(1)
        q2 = quadrants.count(2)
        q3 = quadrants.count(3)
        q4 = quadrants.count(4)

        print(q1*q2*q3*q4)
