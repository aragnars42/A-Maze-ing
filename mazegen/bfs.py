from collections import deque


def bfs_short(maze, start, end):
    queue = deque([start])
    visited = set([start])
    p = {}
    p[start] = None
    directions = [
            {"dx": 0,  "dy": -1, "direc": 0, "opposite": 2}, #up
            {"dx": 0,  "dy": 1,  "direc": 2, "opposite": 0}, #down
            {"dx": -1, "dy": 0,  "direc": 3, "opposite": 1}, #left (esquerda)
            {"dx": 1,  "dy": 0,  "direc": 1, "opposite": 3}, #right (direita)
        ]
    while queue:
        node = queue.popleft()
        new_x, new_y = node
        if (new_x, new_y) == end:
            break
        for d in directions:
            wall = maze.has_wall(new_x, new_y, d["direc"])
            if not wall:
                new_nx = new_x + d["dx"]
                new_ny = new_y + d["dy"]
                if not (
                        0 <= new_nx < maze.width and
                        0 <= new_ny < maze.height):
                    continue
                if (new_nx, new_ny) not in visited:
                    visited.add((new_nx, new_ny))
                    queue.append((new_nx, new_ny))
                    p[(new_nx, new_ny)] = (new_x, new_y)
    pt = []
    if end not in p:
        return None
    new_end = end
    while new_end is not None:
        pt.append(new_end)
        new_end = p[new_end]
    pt.reverse()
    list_diect_str = []
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
