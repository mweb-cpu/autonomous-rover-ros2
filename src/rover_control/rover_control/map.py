import random
# Constants for map representation
EMPTY = "."
ROVER = "R"
GOAL = "G"
OBSTACLE = "X"
VISITED = "*"

class Map:
    """
    Rover's environment
    Responsibilities:
        - Create map
        - Place rover
        - Place goal
        - Place obstacles
        - Track visited squares
        - Display map
    """ 
    
    # generate grid
    def __init__(self, num_obstacles, size=10):
        self.size = size
        self.grid = []
        self.visited = []
        self.previous_x = None
        self.previous_y = None
        

        self.create_grid()
        self.place_obstacles(num_obstacles)

    # create grid with size 10x10
    def create_grid(self):
        for row in range(self.size):
            self.grid.append([EMPTY] * self.size)

    # finds empty squares
    def find_empty_location(self):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.grid[y][x] == EMPTY:
                return x, y
            
    # place rover on grid
    def place_rover(self):
        rover_x, rover_y = self.find_empty_location()
        self.grid[rover_y][rover_x] = ROVER
        self.previous_x = rover_x
        self.previous_y = rover_y
        return rover_x, rover_y
    
    # place goal on grid
    def place_goal(self):
        goal_x, goal_y = self.find_empty_location()
        self.grid[goal_y][goal_x] = GOAL
        return goal_x, goal_y

    # place random obstacles on grid
    def place_obstacles(self, num_obstacles):
        for _ in range(num_obstacles):
            obstacle_x, obstacle_y = self.find_empty_location()
            self.grid[obstacle_y][obstacle_x] = OBSTACLE

    # deletes old rover position and places new one
    def update_rover(self, x, y):
        # add to visited
        if (x,y) not in self.visited:
            self.visited.append((x,y))
        # remove old rover
        if self.previous_x is not None and self.previous_y is not None:
            self.grid[self.previous_y][self.previous_x] = VISITED
        # place rover
        self.grid[y][x] = ROVER
        # update previous position
        self.previous_x = x
        self.previous_y = y

    # sensor asks what's in square
    def get_square(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[y][x]
        else:
            return None

    # check if rover has been there
    def check_visited(self, x, y):
        return (x, y) in self.visited

    # print map
    def display(self):
        for row in self.grid:
            print(" ".join(row))