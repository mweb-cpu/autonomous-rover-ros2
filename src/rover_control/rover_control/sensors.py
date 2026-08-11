from .map import OBSTACLE


class DistanceSensor:

    def __init__(self, world):
        self.world = world

    def read_distance(self, direction, rover_x, rover_y):
        distance = 0

        directions = {
            "NORTH": (0, -1),
            "EAST": (1, 0),
            "SOUTH": (0, 1),
            "WEST": (-1, 0)
        }

        dx, dy = directions[direction]

        x = rover_x + dx
        y = rover_y + dy

        while 0 <= x < self.world.size and 0 <= y < self.world.size:

            if self.world.get_square(x, y) == OBSTACLE:
                return distance + 1

            distance += 1

            x += dx
            y += dy

        return distance