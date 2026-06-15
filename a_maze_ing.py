from typing import Any, Optional as Opt
from mazegen.mazegen import Maze
from mazegen.parse import parse
from mazegen.dfs import MazeGenerator
from mazegen.output import write_maze
from mazegen.bfs import bfs_short
from mazegen.graphics import Graphics


if __name__ == '__main__':
    maze_parse: dict[str, Any] = parse()

    # Generate maze + draw 42 first, then run BFS.
    entry: tuple[int, int] = (maze_parse["ENTRY"][0], maze_parse["ENTRY"][1])
    exit_pos: tuple[int, int] = (maze_parse["EXIT"][0], maze_parse["EXIT"][1])

    # If BFS returns None, regenerate until it finds a
    # valid path so it doesn't go over the logo
    test: Opt[str] = None
    while test is None:
        gen = MazeGenerator(
            maze_parse["WIDTH"],
            maze_parse["HEIGHT"],
            maze_parse.get("SEED")
        )
        gen.generate(entry[0], entry[1])
        if maze_parse["PERFECT"] is False:
            gen.make_imperfect()
        test = bfs_short(gen.maz, entry, exit_pos)

    # Adding graphics to test
    # Function to regenerate maze when pressing Key1
    def regen() -> tuple[Maze, str]:
        """ """
        result: Opt[str] = None
        while result is None:
            gen: MazeGenerator = MazeGenerator(
                maze_parse["WIDTH"],
                maze_parse["HEIGHT"],
                maze_parse.get("SEED")
            )
            gen.generate(entry[0], entry[1])
            if maze_parse['PERFECT'] is False:
                gen.make_imperfect()
            result = bfs_short(gen.maz, entry, exit_pos)
        return gen.maz, result

    gfx: Graphics = Graphics(
        gen.maz,
        (maze_parse["ENTRY"][0], maze_parse["ENTRY"][1]),
        (maze_parse["EXIT"][0], maze_parse["EXIT"][1]),
        test,
        regen_callback=regen
    )
    gfx.render()

    # Write the path found with bfs_short
    write_maze(
        maze_parse["OUTPUT_FILE"],
        gen.maz.get_maze(),
        (maze_parse["ENTRY"][0], maze_parse["ENTRY"][1]),
        (maze_parse["EXIT"][0], maze_parse["EXIT"][1]),
        test)
