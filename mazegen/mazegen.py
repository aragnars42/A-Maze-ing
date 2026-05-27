"""
Maze generation module that handles maze data structure and wall management.
"""

from typing import List


class Maze:
    """Represents a maze grid with wall encoding using hexadecimal values."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: List[List[int]] = [
            [15 for _ in range(width)] for _ in range(height)
        ]

    def open_wall(self, x: int, y: int, direction: int) -> None:
        """
        Open a wall on a specific cell in a given direction.

        Args:
            x: Column index.
            y: Row index.
            direction: Wall direction (0=North, 1=East, 2=South, 3=West).

        Raises:
            IndexError: If coordinates are out of bounds.
            ValueError: If direction is invalid.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        if not (0 <= direction <= 3):
            raise ValueError("Direction must be 0-3")
        self.cells[y][x] &= ~(1 << direction)
    
    def close_wall(self, x: int, y: int, direction: int) -> None:
        """
        Close a wall on a specific cell in a given direction.

        Args:
            x: Column index.
            y: Row index.
            direction: Wall direction (0=North, 1=East, 2=South, 3=West).

        Raises:
            IndexError: If coordinates are out of bounds.
            ValueError: If direction is invalid.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        if not (0 <= direction <= 3):
            raise ValueError("Direction must be 0-3")
        self.cells[y][x] |= (1 << direction)

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        """
        Check if a wall exists in a specific direction.

        Args:
            x: Column index.
            y: Row index.
            direction: Wall direction (0=North, 1=East, 2=South, 3=West).

        Returns:
            True if wall is closed, False if open.

        Raises:
            IndexError: If coordinates are out of bounds.
            ValueError: If direction is invalid.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        if not (0 <= direction <= 3):
            raise ValueError("Direction must be 0-3")
        return (self.cells[y][x] & (1 << direction)) != 0

    def get_cell(self, x: int, y: int) -> int:
        """
        Get the wall encoding for a cell.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            Integer (0-15) representing wall state.

        Raises:
            IndexError: If coordinates are out of bounds.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        return self.cells[y][x]

    def get_maze(self) -> List[List[int]]:
        """
        Get the complete maze grid.

        Returns:
            2D list of integers representing wall states.
        """
        return self.cells
    