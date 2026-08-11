import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

from .map import Map
from .rover import Rover
from .sensors import DistanceSensor


class SensorNode(Node):

    def __init__(self):
        super().__init__("sensor_node")

        self.world = Map(num_obstacles=10)
        self.rover = Rover(self.world)
        self.sensor = DistanceSensor(self.world)

        self.publisher = self.create_publisher(
            Int32,
            "distance_sensor",
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_distance
        )

    def publish_distance(self):

        distance = self.sensor.read_distance(
            self.rover.direction,
            self.rover.x,
            self.rover.y
        )

        msg = Int32()
        msg.data = distance

        self.publisher.publish(msg)

        self.get_logger().info(
            f"Distance: {distance}"
        )


def main(args=None):
    rclpy.init(args=args)

    node = SensorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()