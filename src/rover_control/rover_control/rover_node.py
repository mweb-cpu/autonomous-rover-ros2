from .rover import Rover
from .map import Map
from .planner import Planner

import rclpy
from rclpy.node import Node

class RoverNode(Node):

    def __init__(self):
        super().__init__("rover_node")
        self.get_logger().info("Rover node started")

        self.world = Map(num_obstacles=10)
        self.rover = Rover(self.world)
        self.planner = Planner(self.world)

        self.goal = self.world.place_goal()

        self.get_logger().info(f"Rover starting position: ({self.rover.x}, {self.rover.y})")
        self.get_logger().info(f"Goal position: {self.goal}")
        self.world.display()

        path = self.planner.bfs((self.rover.x, self.rover.y), self.goal)

        if path is not None:
            self.get_logger().info(f"Path found: {path}")
            self.path = path
            self.timer = self.create_timer(1.0, self.move_rover)

        else:
            self.get_logger().info("No path found")

        self.get_logger().info("Rover simulation loaded")

    def move_rover(self):
        if self.path:
            next_position = self.path.pop(0)
            x, y = next_position

            self.rover.move_to(x,y)

            self.get_logger().info(f"Moved to ({x}, {y})")

            self.world.display()

            if (self.rover.x, self.rover.y) == self.goal:
               self.get_logger().info("Rover reached goal")
               self.timer.cancel()

        else:
            self.get_logger().info("Path completed")
            self.world.display()
            self.timer.cancel()

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