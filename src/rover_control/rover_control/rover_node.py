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

        goal = self.world.place_goal()

        self.get_logger().info(f"Rover starting position: ({self.rover.x}, {self.rover.y})")
        self.get_logger().info(f"Goal position: {goal}")
        self.world.display()

        path = self.planner.bfs((self.rover.x, self.rover.y), goal)

        if path is not None:
            self.get_logger().info(f"Path found: {path}")
            self.rover.follow_path(path, self.world)
            self.get_logger().info("Rover reached the goal!")

        else:
            self.get_logger().info("No path found")

        self.world.display()
        self.get_logger().info("Rover simulation loaded")


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