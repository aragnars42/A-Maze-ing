# Maze grid storage and wall bit operations.
from typing import List


class Maze:
    """Stores the maze cells as hex and manages wall states."""
    def __init__(self, width: int, height: int) -> None:
        """Initialize the maze with all cells fully closed (value 15).
 
        Args:
            width: Number of cells horizontally.
            height: Number of cells vertically.
        """
        self.width: int = width
        self.height: int = height
        self.cells: List[List[int]] = [
            [15 for _ in range(width)] for _ in range(height)
        ]

    def open_wall(self, x: int, y: int, direction: int) -> None:
        """Open one wall bit in a cell.
 
        Args:
            x: Cell x coordinate.
            y: Cell y coordinate.
            direction: Wall direction (0=N, 1=E, 2=S, 3=W).
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        if not (0 <= direction <= 3):
            raise ValueError("Direction must be 0-3")
        self.cells[y][x] &= ~(1 << direction)

    def close_wall(self, x: int, y: int, direction: int) -> None:
        """Close one wall bit in a cell.
 
        Args:
            x: Cell x coordinate.
            y: Cell y coordinate.
            direction: Wall direction (0=N, 1=E, 2=S, 3=W).
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        if not (0 <= direction <= 3):
            raise ValueError("Direction must be 0-3")
        self.cells[y][x] |= (1 << direction)

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        """Check whether a wall is present.
 
        Args:
            x: Cell x coordinate.
            y: Cell y coordinate.
            direction: Wall direction (0=N, 1=E, 2=S, 3=W).
 
        Returns:
            True if the wall is closed, False if open.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        if not (0 <= direction <= 3):
            raise ValueError("Direction must be 0-3")
        return (self.cells[y][x] & (1 << direction)) != 0

    def get_cell(self, x: int, y: int) -> int:
        """Return the raw wall value for a cell.
 
        Args:
            x: Cell x coordinate.
            y: Cell y coordinate.
 
        Returns:
            Integer bitmask of closed walls.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        return self.cells[y][x]

    def get_maze(self) -> List[List[int]]:
        """Return the full maze grid as a 2D list.
 
        Returns:
            2D list of cell wall values.
        """
        return self.cells
