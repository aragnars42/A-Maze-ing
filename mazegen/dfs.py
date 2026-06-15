from .mazegen import Maze
from typing import Any
import random


class MazeGenerator:
    """ Maze genaretor 
    
    Atributes:
        Visit: saves already visited cells (to avoid repetition)
        stack: Use it to generate the maze with dfs
        maz: the object of the labyrinth itself
        seed: Define predictable randomness 
        (same maze if the seed is repeated).
        directions: 
            North - top (-1, 0) Y,X
            South - down (1, 0) Y,X
            West - left (0, -1) Y,X
            East - right (0, 1) Y,X
    """
    def __init__(self, width: int, height: int, seed: Any | None) -> None:
        """
        Just function for my parameters than i use in future

        descrever
        Each direction is represented as:
        a dict: 
            dx, dy is displacement:
            North - top (-1, 0) Y,X
            South - down (1, 0) Y,X
            West - left (0, -1) Y,X
            East - right (0, 1) Y,X
            direc: Index of the wall that needs to be removed.
            opposite: opposite wall (used when "making way" 
            between cells)

        Args:
            width (int): maze width
            height (int): maze height
            seed (Any|None): Define predictable randomness (same maze if the seed is repeated).
        """
        self.visit: set[tuple[int, int]] = set()
        self.stack: list[tuple[int, int]] = []
        self.maz: Maze = Maze(width, height)

        if seed is not None:
            random.seed(seed)

        self.directions: list[dict[str, int]] = [
            {"dx": 0,  "dy": -1, "direc": 0, "opposite": 2},
            {"dx": 0,  "dy": 1,  "direc": 2, "opposite": 0},
            {"dx": -1, "dy": 0,  "direc": 3, "opposite": 1},
            {"dx": 1,  "dy": 0,  "direc": 1, "opposite": 3},
        ]

    def get_neighbors(
        self,
        x: int,
        y: int,
        pattern: list[tuple[int, int]]
    ) -> list[tuple[int, int, dict[str, int]]]:
        """
        Returns all valid neighboring 
        cells of a given position in the maze.

        A neighbor is considered valid if:
            It is within the maze boundaries.
            It has not been visited yet.
            It is not present in the given exclusion pattern.
        Each returned neighbor includes its 
        coordinate and the direction
        metadata used to move from the current cell
        to that neighbor.

        Args:
            x (int): Current x-coordinate.
            y (int): Current y-coordinate.
            pattern (list[tuple[int, int]]): List of coordinates to exclude for 42

        Returns:
            list[tuple[int, int, dict[str, int]]]:
                A list of valid neighbors,
                each represented as a tuple
                containing (nx, ny, direction).
        """
        neighbors: list[tuple[int, int, dict[str, int]]] = []
        for d in self.directions:
            nx: int = x + d["dx"]
            ny: int = y + d["dy"]

            if 0 <= nx < self.maz.width and 0 <= ny < self.maz.height:
                if (nx, ny) not in self.visit and (nx, ny) not in pattern:
                    neighbors.append((nx, ny, d))

        return neighbors

    def generate(self, x: int, y: int) -> None:
        """
        Generate my labyrinth, my perfect one.

        first step list of tuples that I have the 42 
        and already closed and centralized, then go as deep as
        possible and back again when there are no more options.
        self.stack.append((x, y) = start point
        while -> continue maze | self.stack[-1] atual cells
        if are open wall between current and neighbor
        Mark neighbor as visited
        Open back wall (double connection)
        Advance to neighbor (push on stack)

        Args:
            x (int): Current x-coordinate.
            y (int): Current y-coordinate.

        """
        num_4: list[tuple[int, int]] = [
            (1, 0), (3, 0),
            (1, 1), (3, 1),
            (1, 2), (2, 2), (3, 2),
            (3, 3),
            (3, 4)
        ]
        num_2: list[tuple[int, int]] = [
            (1, 0), (2, 0), (3, 0),
            (3, 1),
            (1, 2), (2, 2), (3, 2),
            (1, 3),
            (1, 4), (2, 4), (3, 4)
        ]
        center_w: int = self.maz.width // 2 - 5
        center_h: int = self.maz.height // 2 - 2
        pattern: list[tuple[int, int]] = []
        for coord in num_4:
            pattern.append((coord[0] + center_w, coord[1] + center_h))
        for coord in num_2:
            pattern.append((coord[0] + center_w + 5, coord[1] + center_h))

        self.stack.append((x, y))


        while self.stack:
            x, y = self.stack[-1]

            neighbors: list[
                tuple[
                    int,
                    int,
                    dict[
                        str,
                        int
                    ]
                ]
            ] = self.get_neighbors(x, y, pattern)

            if neighbors:
                nx, ny, d = random.choice(neighbors)
                self.maz.open_wall(x, y, d["direc"])

                self.visit.add((nx, ny))
                self.maz.open_wall(nx, ny, d["opposite"])
                self.stack.append((nx, ny))
            else:
                self.stack.pop()
                #back t.t

    def get_neighbors_imperfect(
        self,
        x: int,
        y: int,
        pattern: list[tuple[int, int]]
    ) -> list[dict[str, int]]:
        """
        Similar to my other get_neighbors function,
        but this one returns neighbors who: are inside the maze
        and are not in the pattern

        Unlike "get_neighbors", which only allows me to access new cells,
        here I can go back to older cells if that helps. 
        The 'get_neighbors_imperfect'
        method allows you to revisit cells, creating 
        loops in the maze, while the 'normal' method prevents 
        this to maintain a loop-free maze.
        x, y = where you are
        dx, dy = where you want to go
        nx, ny = where you will end up

        Args:
            x (int): Current x-coordinate.
            y (int): Current y-coordinate.
            pattern (list[tuple[int, int]]):
            List of coordinates to exclude for 42

        Returns:
            list[tuple[int, int, dict[str, int]]]:
                A list of valid neighbors, each represented as a tuple
                containing (nx, ny, direction).
                dx, dy -> where you're going on the grid
                direc -> which wall to open
                opposite -> neighbor's wall (to connect the two sides)
                It does NOT return coordinates directly."""
                
        neighbors: list[dict[str, int]] = []

        for d in self.directions:
            nx: int = x + d["dx"]
            ny: int = y + d["dy"]

            if 0 <= nx < self.maz.width and 0 <= ny < self.maz.height:
                if (nx, ny) not in pattern:
                    neighbors.append(d)

        return neighbors

    def make_imperfect(self, openings: int = 100) -> None:
        """
        Generate my labyrinth, my imperfect one.

        first step list of tuples that I have the 42 
        and already closed and centralized. It transforms 
        a perfect maze into an "imperfect" maze
        (with loops) by opening random walls. 
        The labyrinth already exists (perfect)
        Then it "breaks walls" Creates shortcuts and 
        loops after generation.
        x, y = where you are
        dx, dy = where you want to go
        nx, ny = where you will end up
 
        Args:
            opening (int) There are 100 tentative
            tents in the walls without labour
        """
        num_4: list[tuple[int, int]] = [
            (1, 0), (3, 0),
            (1, 1), (3, 1),
            (1, 2), (2, 2), (3, 2),
            (3, 3),
            (3, 4)
        ]
        num_2: list[tuple[int, int]] = [
            (1, 0), (2, 0), (3, 0),
            (3, 1),
            (1, 2), (2, 2), (3, 2),
            (1, 3),
            (1, 4), (2, 4), (3, 4)
        ]
        center_w: int = self.maz.width // 2 - 5
        center_h: int = self.maz.height // 2 - 2
        pattern: list[tuple[int, int]] = []
        for coord in num_4:
            pattern.append((coord[0] + center_w, coord[1] + center_h))
        for coord in num_2:
            pattern.append((coord[0] + center_w + 5, coord[1] + center_h))

        for _ in range(openings):
            x, y = pattern[0]
            while (x, y) in pattern:
                x = random.randint(0, self.maz.width - 1)
                y = random.randint(0, self.maz.height - 1)

            directions: list[dict[str, int]] = self.get_neighbors_imperfect(
                x,
                y,
                pattern
            )
            random.shuffle(directions)
            for d in directions:
                nx: int = x + d["dx"]
                ny: int = y + d["dy"]
                # I apply movement to my cell.

                if not (
                        0 <= nx < self.maz.width and
                        0 <= ny < self.maz.height):
                    continue

                if self.maz.has_wall(x, y, d["direc"]):
                    self.maz.open_wall(x, y, d["direc"])
                    self.maz.open_wall(nx, ny, d["opposite"])
                    break

    def check_wall(self) -> None:
        """
        check 2x2

        This function traverses the maze in 2x2
        blocks and closes walls when it
        encounters areas that are too open, in order
        to improve the maze's structure.
        """
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
