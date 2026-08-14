# Constants for directions
DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]

class Rover:
    """
    Rover's movement and status
    Responsibilities:
        - Holds direction and position
        - Moves rover
        - Turns rover
        - Avoids obstacles, edges, and visited squares
        - Tracks battery level
        - Displays rover status
    """ 
    
    # starting conditions
    def __init__(self, world):
        self.world = world
        self.x, self.y = self.world.place_rover()
        self.direction = "NORTH"
        self.battery = 100

    # moves rover to coordinates
    def move_to(self, x, y):
        self.world.update_rover(x,y)

        # Determine direction based on movement
        if x > self.x:
            self.direction = "EAST"
        elif x < self.x:
            self.direction = "WEST"
        elif y > self.y:
            self.direction = "SOUTH"
        elif y < self.y:
            self.direction = "NORTH"

        self.x = x
        self.y = y

    # turns rover left or right and decreases battery
    def turn_left(self):
        current = DIRECTIONS.index(self.direction)
        self.direction = DIRECTIONS[(current - 1) % len(DIRECTIONS)]
        self.use_battery()

    def turn_right(self):
        current = DIRECTIONS.index(self.direction)
        self.direction = DIRECTIONS[(current + 1) % len(DIRECTIONS)]
        self.use_battery()

    # Changes position of rover and decrease battery
    def move(self):
        if self.direction == "NORTH":
            self.y -= 1
        elif self.direction == "SOUTH":
            self.y += 1
        elif self.direction == "EAST":
            self.x += 1
        elif self.direction == "WEST":
            self.x -= 1
        self.use_battery()

    # returns rover's status
    def status(self):
        return f"Rover Position: ({self.x}, {self.y}) \nDirection: {self.direction} \nBattery: {self.battery}%"

    # avoids obstacles, edges, and visited squares by turning left
    def avoid_obstacle(self, sensor_result):
        if sensor_result in ["OBSTACLE", "EDGE", "VISITED"]:
            print(f"Encountered {sensor_result}. Turning left.")
            self.turn_left()
        else:
            print("Path is clear.")
            self.move()

    # makes sure battery doesn't go below 0
    def use_battery(self):
        if self.battery > 0:
            self.battery -= 1
        else:
            print("Battery is empty. Rover cannot move.")

    # reset rover's position, direction, and battery level
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.direction = "SOUTH"
        self.battery = 100

    # rover follows path to goal
    def follow_path(self, path, world):
        print("====== FOLLOWING PATH ======")
        print(path)
        for position in path[1:]:
            while (self.x, self.y) != position:
                print("---------------------------")
                if self.x < position[0]:
                    self.face_direction("EAST")
                elif self.x > position[0]:
                    self.face_direction("WEST")
                elif self.y < position[1]:
                    self.face_direction("SOUTH")
                elif self.y > position[1]:
                    self.face_direction("NORTH")
                self.move()
                world.update_rover(self.x, self.y)
                print(f"Moving FORWARD")
                print(self.status())
        print("======= GOAL REACHED =======")

    # helps rover face the right direction
    def face_direction(self, target_direction):
        while self.direction != target_direction:
            self.turn_right()
            print(f"Turning {target_direction}")