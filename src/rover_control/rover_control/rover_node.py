import rclpy
from rclpy.node import Node

class RoverNode(Node):

    def __init__(self):
        super().__init__("rover_node")
        self.get_logger().info("Rover node started")

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