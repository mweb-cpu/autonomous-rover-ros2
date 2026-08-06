from collections import deque

from .map import OBSTACLE

DIRECTIONS = [
    (0,-1), # North
    (1,0),  # East
    (0,1),  # South
    (-1,0)  # West
]

class Planner:
    def __init__(self, world):
        self.world = world

    def bfs(self, start, goal):
        """
        Finds shortest path from start to goal using BFS algorithm

        Returns:
            - list of coordinates from start to goal
            - Returns None if no path is found
        """

        queue = deque([start])
        visited = set()
        visited.add(start)
        parent = {}

        while queue:
            current = queue.popleft()

            if current == goal:
                return self._reconstruct_path(parent, start, goal)

            for neighbor in self._get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return None
    # returns all valid neighbors (not obstacles or edge)
    def _get_neighbors(self, position):
        x, y = position
        neighbors = []

        for dx, dy in DIRECTIONS:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < self.world.size and 0 <= ny < self.world.size:
                if self.world.get_square(nx, ny) != OBSTACLE:
                    neighbors.append((nx, ny))
        return neighbors

    def _reconstruct_path(self, parent, start, goal):
        path = []
        current = goal

        while current != start:
            path.append(current)
            current = parent[current]

        path.append(start)
        path.reverse()
        return path