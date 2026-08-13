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
            self.path = path
            self.timer = self.create_timer(
                1.0, 
                self.move_rover
            )

        else:
            self.get_logger().info("No path found")

        self.get_logger().info("Rover simulation loaded") # debug

    def move_rover(self):
        if self.path:
            # Get Next Position
            x, y = self.path.pop(0)

            # Move Rover
            self.rover.move_to(x,y)

            # Publish Rover Information
            self.publish_map()
            self.publish_position()
            self.publish_direction()

            # Display Updated Map
            self.get_logger().info(
                f"Moved to ({x}, {y})"
            )
            self.world.display()

            # Check Goal
            if (self.rover.x, self.rover.y) == self.goal:
               self.get_logger().info("Rover reached goal")
               self.timer.cancel()

        else:
            self.get_logger().info("Path completed")
            self.world.display()
            self.timer.cancel()

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

    def sensor_callback(self, msg):
        distance = msg.data
        self.get_logger().info(f"Rover received sensor distance: {distance}")

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