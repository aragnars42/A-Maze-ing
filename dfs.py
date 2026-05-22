from mazegen import Maze
import random


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.visit = set()
        self.stack = []
        self.maz = Maze(width, height)

        if seed is not None:
            random.seed(seed)

        self. directions = [
            {"dx": 0,  "dy": -1, "direc": 0, "opposite": 2}, #up
            {"dx": 0,  "dy": 1,  "direc": 2, "opposite": 0}, #down
            {"dx": -1, "dy": 0,  "direc": 3, "opposite": 1}, #left (esquerda)
            {"dx": 1,  "dy": 0,  "direc": 1, "opposite": 3}, #right (direita)
        ]

    def get_neighbors(self, x, y) -> None:
        neighbors = []

        for d in self.directions:
            nx = x + d["dx"]
            ny = y + d["dy"]

            if 0 <= nx < self.maz.width and 0 <= ny < self.maz.height:
                if (nx, ny) not in self.visit:
                    neighbors.append((nx, ny, d))

        return neighbors

    def generate(self, x: int, y: int) -> None:
        self.visit.add((x, y))
        self.stack.append((x, y))

        while self.stack:
            x, y = self.stack[-1]

            neighbors = self.get_neighbors(x, y)

            if neighbors:
                nx, ny, d = random.choice(neighbors)
                self.maz.open_wall(x, y, d["direc"])

                self.visit.add((nx, ny))
                self.maz.open_wall(nx, ny, d["opposite"])
                self.stack.append((nx, ny))
            else:
                self.stack.pop()
