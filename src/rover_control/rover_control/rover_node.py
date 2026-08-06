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