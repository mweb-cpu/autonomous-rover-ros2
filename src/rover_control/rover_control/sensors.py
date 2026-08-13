from .map import OBSTACLE


class DistanceSensor:
    # Movement offsets for each direction
    DIRECTIONS = {
        "NORTH": (0, -1),
        "EAST": (1, 0),
        "SOUTH": (0, 1),
        "WEST": (-1, 0)
    }

    def __init__(self, world):
        self.world = world

    def read_distance(self, direction, rover_x, rover_y):
        """
        Measure the distance from the rover to the nearest obstacle
        in the direction the rover is facing.

        Returns:
            Distance to the nearest obstacle.
            If there is no obstacle before the edge of the map,
            returns the distance to the edge.
        """

        distance = 0

        dx, dy = self.DIRECTIONS[direction]

        x = rover_x + dx
        y = rover_y + dy

        while 0 <= x < self.world.size and 0 <= y < self.world.size:

            if self.world.get_square(x, y) == OBSTACLE:
                return distance + 1

            distance += 1

            x += dx
            y += dy

        return distance