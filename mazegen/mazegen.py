# Maze grid storage and wall bit operations.
from typing import List


# Stores the maze cells as hex and manages wall states.
class Maze:
    # Start with every cell closed (value 15).
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.cells: List[List[int]] = [
            [15 for _ in range(width)] for _ in range(height)
        ]

    # Open one wall bit in a cell.
    def open_wall(self, x: int, y: int, direction: int) -> None:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        if not (0 <= direction <= 3):
            raise ValueError("Direction must be 0-3")
        self.cells[y][x] &= ~(1 << direction)

    # Close one wall bit in a cell.
    def close_wall(self, x: int, y: int, direction: int) -> None:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        if not (0 <= direction <= 3):
            raise ValueError("Direction must be 0-3")
        self.cells[y][x] |= (1 << direction)

    # Check whether a wall is present.
    def has_wall(self, x: int, y: int, direction: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        if not (0 <= direction <= 3):
            raise ValueError("Direction must be 0-3")
        return (self.cells[y][x] & (1 << direction)) != 0

    # Return the raw wall value for a cell.
    def get_cell(self, x: int, y: int) -> int:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        return self.cells[y][x]

    # Return the full maze grid as 2D list.
    def get_maze(self) -> List[List[int]]:
        return self.cells
