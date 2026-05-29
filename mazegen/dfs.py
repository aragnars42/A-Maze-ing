from mazegen.mazegen import Maze
import random


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.visit = set()
        self.stack = []
        self.maz = Maze(width, height)

        if seed is not None:
            random.seed(seed)

        self.directions = [
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

    def draw(self):
        num_4 = [
            (1,0), (3,0),
            (1,1), (3,1),
            (1,2), (2,2), (3,2),
            (3,3),
            (3,4)
        ]
        num_2 = [
            (1,0),(2,0),(3,0),
            (3,1),
            (1,2),(2,2),(3,2),
            (1,3),
            (1,4),(2,4),(3,4)
        ]
        center_w = self.maz.width // 2 - 5
        center_h = self.maz.height // 2 - 5
    
        for dx, dy in num_4:
            x = center_w + dx
            y = center_h + dy
            self.maz.close_wall(x, y, 0)
            self.maz.close_wall(x, y, 1)
            self.maz.close_wall(x, y, 2)
            self.maz.close_wall(x, y, 3)

        for xd, yd in num_2: 
            xx = center_w + xd + 5
            yy = center_h + yd
            self.maz.close_wall(xx, yy, 0)
            self.maz.close_wall(xx, yy, 1)
            self.maz.close_wall(xx, yy, 2)
            self.maz.close_wall(xx, yy, 3)

    def check_wall(self):
        for x in range(self.maz.width - 2):        
            for y in range(self.maz.height - 2):
                if (not self.maz.has_wall(x, y, 1) and not
                self.maz.has_wall(x+1, y, 1) and not
                self.maz.has_wall(x, y+1, 1) and not 
                self.maz.has_wall(x+1, y+1, 1) and not
                self.maz.has_wall(x, y, 2) and not
                self.maz.has_wall(x+1, y, 2) and not
                self.maz.has_wall(x, y+1, 2) and not 
                self.maz.has_wall(x+1, y+1, 2)):
                    self.maz.close_wall(x+1, y, 1)
                    self.maz.close_wall(x+2, y, 3)
