import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String
from geometry_msgs.msg import Point

from .sensors import DistanceSensor
from .map import Map

class SensorNode(Node):

    def __init__(self):
        super().__init__("sensor_node")

        self.world = None
        self.sensor = DistanceSensor(self.world)

        self.rover_x = 0
        self.rover_y = 0
        self.rover_direction = "NORTH"

        self.position_subscription = self.create_subscription(
            Point,
            "rover_position",
            self.position_callback,
            10
        )

        self.direction_subscription = self.create_subscription(
            String,
            "rover_direction",
            self.direction_callback,
            10
        )

        self.map_subscription = self.create_subscription(
            String,
            "rover_map",
            self.map_callback,
            10
        )

        self.publisher = self.create_publisher(
            Int32,
            "distance_sensor",
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_distance
        )

    def position_callback(self, msg):
        self.rover_x = int(msg.x)
        self.rover_y = int(msg.y)

    def direction_callback(self, msg):
        self.rover_direction = msg.data

    def map_callback(self, msg):
        self.get_logger().info("Map received")

        rows = msg.data.split("\n")

        self.world = Map(num_obstacles=0, size=len(rows))
        self.world.grid = [list(row) for row in rows]

        self.sensor.world = self.world
        self.get_logger().info("Sensor map updated")

    def publish_distance(self):

        self.get_logger().info("Sensor timer running")

        if self.world is None:
            self.get_logger().info("Waiting for map...")
            return

        self.get_logger().info(
            f"Reading at ({self.rover_x}, {self.rover_y}) facing {self.rover_direction}"
        )

        distance = self.sensor.read_distance(
            self.rover_direction,
            self.rover_x,
            self.rover_y
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