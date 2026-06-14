from .mazegen import Maze
import random


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.visit = set()
        self.stack = []
        self.maz = Maze(width, height)

        if seed is not None:
            random.seed(seed)

        self.directions = [
            {"dx": 0,  "dy": -1, "direc": 0, "opposite": 2},
            {"dx": 0,  "dy": 1,  "direc": 2, "opposite": 0},
            {"dx": -1, "dy": 0,  "direc": 3, "opposite": 1},
            {"dx": 1,  "dy": 0,  "direc": 1, "opposite": 3},
        ]

    def get_neighbors(self, x, y, pattern: list) -> list:
        neighbors = []

        for d in self.directions:
            nx = x + d["dx"]
            ny = y + d["dy"]

            if 0 <= nx < self.maz.width and 0 <= ny < self.maz.height:
                if (nx, ny) not in self.visit and (nx, ny) not in pattern:
                    neighbors.append((nx, ny, d))

        return neighbors

    def generate(self, x: int, y: int) -> None:
        num_4 = [
            (1, 0), (3, 0),
            (1, 1), (3, 1),
            (1, 2), (2, 2), (3, 2),
            (3, 3),
            (3, 4)
        ]
        num_2 = [
            (1, 0), (2, 0), (3, 0),
            (3, 1),
            (1, 2), (2, 2), (3, 2),
            (1, 3),
            (1, 4), (2, 4), (3, 4)
        ]
        center_w = self.maz.width // 2 - 5
        center_h = self.maz.height // 2 - 2
        pattern = []
        for coord in num_4:
            pattern.append((coord[0] + center_w, coord[1] + center_h))
        for coord in num_2:
            pattern.append((coord[0] + center_w + 5, coord[1] + center_h))

        self.stack.append((x, y))

        while self.stack:
            x, y = self.stack[-1]

            neighbors = self.get_neighbors(x, y, pattern)

            if neighbors:
                nx, ny, d = random.choice(neighbors)
                self.maz.open_wall(x, y, d["direc"])

                self.visit.add((nx, ny))
                self.maz.open_wall(nx, ny, d["opposite"])
                self.stack.append((nx, ny))
            else:
                self.stack.pop()

    def get_neighbors_imperfect(self, x, y, pattern: list) -> list:
        neighbors = []

        for d in self.directions:
            nx = x + d["dx"]
            ny = y + d["dy"]

            if 0 <= nx < self.maz.width and 0 <= ny < self.maz.height:
                if (nx, ny) not in pattern:
                    neighbors.append(d)
                    # return directions

        return neighbors

    def make_imperfect(self, openings: int = 100) -> None:
        num_4 = [
            (1, 0), (3, 0),
            (1, 1), (3, 1),
            (1, 2), (2, 2), (3, 2),
            (3, 3),
            (3, 4)
        ]
        num_2 = [
            (1, 0), (2, 0), (3, 0),
            (3, 1),
            (1, 2), (2, 2), (3, 2),
            (1, 3),
            (1, 4), (2, 4), (3, 4)
        ]
        center_w = self.maz.width // 2 - 5
        center_h = self.maz.height // 2 - 2
        pattern = []
        for coord in num_4:
            pattern.append((coord[0] + center_w, coord[1] + center_h))
        for coord in num_2:
            pattern.append((coord[0] + center_w + 5, coord[1] + center_h))

        for _ in range(openings):
            x, y = pattern[0]
            while (x, y) in pattern:
                x = random.randint(0, self.maz.width - 1)
                y = random.randint(0, self.maz.height - 1)

            directions = self.get_neighbors_imperfect(x, y, pattern)
            random.shuffle(directions)
            for d in directions:
                nx = x + d["dx"]
                ny = y + d["dy"]

                if not (
                        0 <= nx < self.maz.width and
                        0 <= ny < self.maz.height):
                    continue

                if self.maz.has_wall(x, y, d["direc"]):
                    self.maz.open_wall(x, y, d["direc"])
                    self.maz.open_wall(nx, ny, d["opposite"])
                    break

    def check_wall(self):
        for x in range(self.maz.width - 2):
            for y in range(self.maz.height - 2):
                if (
                    not self.maz.has_wall(x, y, 1) and not
                    self.maz.has_wall(x+1, y, 1) and not
                    self.maz.has_wall(x, y+1, 1) and not
                    self.maz.has_wall(x+1, y+1, 1) and not
                    self.maz.has_wall(x, y, 2) and not
                    self.maz.has_wall(x+1, y, 2) and not
                    self.maz.has_wall(x, y+1, 2) and not
                    self.maz.has_wall(x+1, y+1, 2)
                ):
                    self.maz.close_wall(x+1, y, 1)
                    self.maz.close_wall(x+2, y, 3)
