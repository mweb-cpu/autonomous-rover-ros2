from .rover import Rover
from .map import Map
from .planner import Planner

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import Int32, String

class RoverNode(Node):

    def __init__(self):
        super().__init__("rover_node")
        self.get_logger().info("Rover node started") # debug

        # Builds Rover Environment
        self.world = Map(num_obstacles=10)
        self.rover = Rover(self.world)
        self.planner = Planner(self.world)

        # Place Goal
        self.goal = self.world.place_goal()
        self.sensor_distance = None

        # ROS2 Publishers
        self.position_publisher = self.create_publisher(
            Point, 
            "rover_position", 
            10
        )
        self.direction_publisher = self.create_publisher(
            String, 
            "rover_direction", 
            10
        )
        self.map_publisher = self.create_publisher(
            String, 
            "rover_map", 
            10
        )
        self.path_publisher = self.create_publisher(
            String,
            "rover_path",
            10
        )

        # ROS2 Subscriber
        self.sensor_subscription = self.create_subscription(
            Int32, 
            "distance_sensor", 
            self.sensor_callback, 
            10
        )

        # Displays Initial Conditions & Environment
        self.get_logger().info(
            f"Rover starting position: ({self.rover.x}, {self.rover.y})"
        )
        self.get_logger().info(
            f"Goal position: {self.goal}"
        )
        self.world.display()

        # Find Path
        path = self.planner.bfs((self.rover.x, self.rover.y), self.goal)

        # Implement Path
        if path is not None:
            self.get_logger().info(
                f"Path found: {path}"
            )
            self.path = path[1:]
            self.publish_path()
            self.timer = self.create_timer(
                1.0, 
                self.move_rover
            )

        else:
            self.get_logger().info("No path found")

        self.get_logger().info("Rover simulation loaded") # debug

    def move_rover(self):

        # Check the sensor before moving
        if self.sensor_distance == 1:

            self.get_logger().info(
                "Obstacle detected! Replanning..."
            )

            # Add the detected obstacle to the map
            self.update_obstacle_from_sensor()

            # Find a new path
            if not self.replan():

                self.get_logger().info(
                    "Rover cannot reach the goal."
                )

                self.timer.cancel()
                return

        # Follow the current path
        if self.path:

            next_position = self.path.pop(0)
            x, y = next_position

            self.rover.move_to(x, y)

            self.publish_map()
            self.publish_position()
            self.publish_direction()

            self.get_logger().info(
                f"Moved to ({x}, {y})"
            )

            self.world.display()

            # Check if rover reached the goal
            if (self.rover.x, self.rover.y) == self.goal:

                self.get_logger().info(
                    "Rover reached goal"
                )

                self.timer.cancel()

        else:

            self.get_logger().info(
                "Path completed"
            )

            self.world.display()
            self.timer.cancel()

    def decide_direction(self):

        x = self.rover.x
        y = self.rover.y

        # Check the squares to the left and right
        if self.rover.direction == "NORTH":
            left = (x - 1, y)
            right = (x + 1, y)

        elif self.rover.direction == "EAST":
            left = (x, y - 1)
            right = (x, y + 1)

        elif self.rover.direction == "SOUTH":
            left = (x + 1, y)
            right = (x - 1, y)

        else:  # WEST
            left = (x, y + 1)
            right = (x, y - 1)

        # Check whether the locations are valid
        left_clear = (
            0 <= left[0] < self.world.size
            and 0 <= left[1] < self.world.size
            and self.world.get_square(*left) != "X"
        )

        right_clear = (
            0 <= right[0] < self.world.size
            and 0 <= right[1] < self.world.size
            and self.world.get_square(*right) != "X"
        )

        if left_clear:
            self.get_logger().info(
                f"Obstacle ahead. Left is clear: {left}"
            )
            return "LEFT"

        elif right_clear:
            self.get_logger().info(
                f"Obstacle ahead. Right is clear: {right}"
            )
            return "RIGHT"

        else:
            self.get_logger().info(
                "Obstacle ahead. No immediate alternatives."
            )
            return None

    def update_obstacle_from_sensor(self):

        directions = {
            "NORTH": (0, -1),
            "EAST": (1, 0),
            "SOUTH": (0, 1),
            "WEST": (-1, 0)
        }

        dx, dy = directions[self.rover.direction]

        obstacle_x = self.rover.x + dx
        obstacle_y = self.rover.y + dy

        # Make sure the location is inside the map
        if (
            0 <= obstacle_x < self.world.size
            and 0 <= obstacle_y < self.world.size
        ):
            self.world.grid[obstacle_y][obstacle_x] = "X"

            self.get_logger().info(
                f"Updated map: obstacle at "
                f"({obstacle_x}, {obstacle_y})"
            )

    def replan(self):

        start = (self.rover.x, self.rover.y)

        new_path = self.planner.bfs(
            start,
            self.goal
        )

        if new_path is None:

            self.get_logger().info(
                "No new path to goal."
            )

            return False

        self.path = new_path[1:]

        self.get_logger().info(
            f"New path found: {new_path}"
        )

        self.publish_path()

        return True

    def publish_position(self):

        msg = Point()

        msg.x = float(self.rover.x)
        msg.y = float(self.rover.y)
        msg.z = 0.0

        self.position_publisher.publish(msg)

    def publish_direction(self):

        msg = String()
        msg.data = self.rover.direction

        self.direction_publisher.publish(msg)

    def publish_map(self):
        msg = String()

        map_data = "\n".join(
            "".join(row) for row in self.world.grid
        )

        msg.data = map_data

        self.map_publisher.publish(msg)

    def publish_path(self):
        msg = String()

        path_data = "\n".join(
            f"{x},{y}"
            for x, y in self.path
        )

        msg.data = path_data

        self.path_publisher.publish(msg)

    def sensor_callback(self, msg):
        self.sensor_distance = msg.data
        self.get_logger().info(
            f"Rover received sensor distance: {self.sensor_distance}"
        )

def main(args=None):
    rclpy.init(args=args)

    node = RoverNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()