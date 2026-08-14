import tkinter as tk

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32, String
from geometry_msgs.msg import Point


class RoverVisualizer(Node):

    def __init__(self):
        super().__init__("rover_visualizer")

        # GUI settings
        self.cell_size = 50

        # Current rover information
        self.rover_x = None
        self.rover_y = None
        self.rover_direction = "NORTH"
        self.sensor_distance = None

        # Current map
        self.grid = None

        # Subscribe to the rover's map
        self.map_subscription = self.create_subscription(
            String,
            "rover_map",
            self.map_callback,
            10
        )

        # Subscribe to the rover's position
        self.position_subscription = self.create_subscription(
            Point,
            "rover_position",
            self.position_callback,
            10
        )

        # Subscribe to the rover's direction
        self.direction_subscription = self.create_subscription(
            String,
            "rover_direction",
            self.direction_callback,
            10
        )

        # Subscribe to the distance sensor
        self.sensor_subscription = self.create_subscription(
            Int32,
            "distance_sensor",
            self.sensor_callback,
            10
        )

        # Create GUI
        self.root = tk.Tk()
        self.root.title("Autonomous Rover")
        self.root.resizable(False, False)

        # Map display
        self.canvas = tk.Canvas(
            self.root,
            width=500,
            height=500
        )

        self.canvas.pack(padx=10, pady=10)

        # Information panel
        self.info_label = tk.Label(
            self.root,
            text="Waiting for rover...",
            font=("Arial", 12),
            justify="left"
        )

        self.info_label.pack(pady=(0, 10))

        # Update GUI periodically
        self.root.after(100, self.update_gui)

    # Receive the rover's map
    def map_callback(self, msg):

        rows = msg.data.split("\n")

        self.grid = [
            list(row)
            for row in rows
        ]

        # Adjust canvas size to the map
        map_size = len(self.grid)

        self.canvas.config(
            width=map_size * self.cell_size,
            height=map_size * self.cell_size
        )

    # Receive the rover's position
    def position_callback(self, msg):

        self.rover_x = int(msg.x)
        self.rover_y = int(msg.y)

    # Receive the rover's direction
    def direction_callback(self, msg):

        self.rover_direction = msg.data

    # Receive the sensor distance
    def sensor_callback(self, msg):

        self.sensor_distance = msg.data

    # Draw the current map
    def draw_map(self):

        if self.grid is None:
            return

        self.canvas.delete("all")

        map_size = len(self.grid)

        for y in range(map_size):
            for x in range(map_size):

                cell = self.grid[y][x]

                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Default cell
                fill = "white"

                if cell == "X":
                    fill = "black"

                elif cell == "R":
                    fill = "blue"

                elif cell == "G":
                    fill = "green"

                elif cell == "*":
                    fill = "lightgray"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill,
                    outline="gray"
                )

        # Draw rover direction indicator
        if self.rover_x is not None and self.rover_y is not None:

            center_x = (
                self.rover_x * self.cell_size
                + self.cell_size / 2
            )

            center_y = (
                self.rover_y * self.cell_size
                + self.cell_size / 2
            )

            arrow_length = 15

            if self.rover_direction == "NORTH":
                end_x = center_x
                end_y = center_y - arrow_length

            elif self.rover_direction == "EAST":
                end_x = center_x + arrow_length
                end_y = center_y

            elif self.rover_direction == "SOUTH":
                end_x = center_x
                end_y = center_y + arrow_length

            else:
                end_x = center_x - arrow_length
                end_y = center_y

            self.canvas.create_line(
                center_x,
                center_y,
                end_x,
                end_y,
                width=4,
                arrow=tk.LAST
            )

    # Update the GUI
    def update_gui(self):

        self.draw_map()

        if self.rover_x is None:

            self.info_label.config(
                text="Waiting for rover..."
            )

        else:

            distance = self.sensor_distance

            if distance is None:
                distance_text = "Waiting..."
            else:
                distance_text = str(distance)

            self.info_label.config(
                text=(
                    f"Position: ({self.rover_x}, {self.rover_y})\n"
                    f"Direction: {self.rover_direction}\n"
                    f"Sensor distance: {distance_text}"
                )
            )

        # Process ROS 2 messages
        rclpy.spin_once(
            self,
            timeout_sec=0
        )

        # Run again in 100 milliseconds
        self.root.after(100, self.update_gui)

    def run(self):

        try:
            self.root.mainloop()

        finally:
            self.destroy_node()

def main(args=None):

    rclpy.init(args=args)

    visualizer = RoverVisualizer()

    visualizer.run()

    rclpy.shutdown()

if __name__ == "__main__":
    main()