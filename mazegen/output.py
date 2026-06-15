# Writes the maze grid, entry/exit, and path to the output file.
from typing import List, Tuple


def write_maze(
    filename: str,
    maze_grid: List[List[int]],
    entry: Tuple[int, int],
    exit_pos: Tuple[int, int],
    path: str
) -> None:
    """Save the maze as hex rows plus entry, exit, and shortest path.
 
    Args:
        filename: Path to the output file.
        maze_grid: 2D list of cell wall values.
        entry: Entry cell coordinates (x, y).
        exit_pos: Exit cell coordinates (x, y).
        path: Solution path string using N/S/E/W characters.
    """
    try:
        with open(filename, 'w') as f:
            for row in maze_grid:
                hex_line: str = ""
                for cell in row:
                    hex_line += format(cell, 'x')
                f.write(hex_line + "\n")
            f.write("\n")
            f.write(str(entry[0]) + "," + str(entry[1]) + "\n")
            f.write(str(exit_pos[0]) + "," + str(exit_pos[1]) + "\n")
            if path is None or path == "":
                f.write("NO PATH\n")
            else:
                f.write(path + "\n")
    except IOError as e:
        print("ERROR - Failed to write:", e)
