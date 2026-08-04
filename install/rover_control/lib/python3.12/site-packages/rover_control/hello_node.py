import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HelloNode(Node):

    def __init__(self):
        super().__init__("hello_node")
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 100

    def timer_callback(self):
        msg = String()
        msg.data = 'Battery: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i -= 1

def main(args=None):
    rclpy.init(args=args)

    hello_node = HelloNode()

    rclpy.spin(hello_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    hello_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()