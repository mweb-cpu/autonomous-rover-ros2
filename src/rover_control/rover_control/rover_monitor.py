import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point


class RoverMonitor(Node):

    def __init__(self):
        super().__init__("rover_monitor")

        self.subscription = self.create_subscription(
            Point,
            "rover_position",
            self.position_callback,
            10
        )

    def position_callback(self, msg):
        self.get_logger().info(
            f"Rover position: ({msg.x}, {msg.y})"
        )


def main(args=None):
    rclpy.init(args=args)

    node = RoverMonitor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()