from parse import parse
from dfs import MazeGenerator
from output import write_maze
from bfs import bfs_short


if __name__ == '__main__':
    maze_parse = parse()

    # create random grid with random, walls
    gen = MazeGenerator(
        maze_parse["WIDTH"],
        maze_parse["HEIGHT"],
        maze_parse.get("SEED"))

    # open up walls from the ENTRY
    gen.generate(maze_parse["ENTRY"][0], maze_parse["ENTRY"][1])

    # find path to connect the entry to the eit
    test = bfs_short(
        gen.maz, (maze_parse["ENTRY"][0], maze_parse["ENTRY"][1]),
        (maze_parse["EXIT"][0], maze_parse["EXIT"][1]))

    # write the path found with bfs_short
    write_maze(
        maze_parse["OUTPUT_FILE"],
        gen.maz.get_maze(),
        (maze_parse["ENTRY"][0], maze_parse["ENTRY"][1]),
        (maze_parse["EXIT"][0], maze_parse["EXIT"][1]),
        test)
