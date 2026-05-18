"""
Maze output module that handles writing maze data to files in hexadecimal format.
"""

from typing import List, Tuple


def write_maze(filename: str, maze_grid: List[List[int]], entry: Tuple[int, int], exit_pos: Tuple[int, int], path: str) -> None:
    """
    Write maze to file in hexadecimal format with entry, exit, and path.

    Args:
        filename: Output filename.
        maze_grid: 2D list of integers (0-15) representing cells.
        entry: Tuple (x, y) of entry coordinates.
        exit_pos: Tuple (x, y) of exit coordinates.
        path: String of directions (N, E, S, W) representing shortest path.

    Returns:
        None

    Raises:
        IOError: If file cannot be written.
    """
    try:
        with open(filename, 'w') as f:
            for row in maze_grid:
                hex_line = ""
                for cell in row:
                    hex_digit = format(cell, 'x')
                    hex_line = hex_line + hex_digit
                f.write(hex_line + "\n")
            f.write("\n")
            f.write(str(entry[0]) + "," + str(entry[1]) + "\n")
            f.write(str(exit_pos[0]) + "," + str(exit_pos[1]) + "\n")
            f.write(path + "\n")
    except IOError as e:
        print("ERROR - Failed to write:", e)