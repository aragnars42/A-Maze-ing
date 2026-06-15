from collections import deque
from typing import Optional as Opt
from .mazegen import Maze


def bfs_short(
    maze: Maze,
    start: tuple[int, int],
    end: Opt[tuple[int, int]]
) -> Opt[str]:
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    
    """
    queue: deque[tuple[int, int]] = deque([start])
    visited: set[tuple[int, int]] = set([start])
    p: dict[tuple[int, int], Opt[tuple[int, int]]] = {}
    p[start] = None
    directions: list[dict[str, int]] = [
            {"dx": 0,  "dy": -1, "direc": 0, "opposite": 2},
            {"dx": 0,  "dy": 1,  "direc": 2, "opposite": 0},
            {"dx": -1, "dy": 0,  "direc": 3, "opposite": 1},
            {"dx": 1,  "dy": 0,  "direc": 1, "opposite": 3},
        ]
    while queue:
        node: tuple[int, int] = queue.popleft()
        new_x, new_y = node
        if (new_x, new_y) == end:
            break
        for d in directions:
            wall: bool = maze.has_wall(new_x, new_y, d["direc"])
            if not wall:
                new_nx: int = new_x + d["dx"]
                new_ny: int = new_y + d["dy"]
                if not (
                        0 <= new_nx < maze.width and
                        0 <= new_ny < maze.height):
                    continue
                if (new_nx, new_ny) not in visited:
                    visited.add((new_nx, new_ny))
                    queue.append((new_nx, new_ny))
                    p[(new_nx, new_ny)] = (new_x, new_y)
    pt: list[tuple[int, int]] = []
    if end not in p:
        return None
    new_end: Opt[tuple[int, int]] = end
    while new_end is not None:
        pt.append(new_end)
        new_end = p[new_end]
    pt.reverse()
    list_diect_str: list[str] = []
    for i in range(len(pt) - 1):
        if pt[i][0] > pt[i+1][0]:
            list_diect_str.append("W")
        if pt[i][0] < pt[i+1][0]:
            list_diect_str.append("E")
        if pt[i][1] > pt[i+1][1]:
            list_diect_str.append("N")
        if pt[i][1] < pt[i+1][1]:
            list_diect_str.append("S")
    return "".join(list_diect_str)
