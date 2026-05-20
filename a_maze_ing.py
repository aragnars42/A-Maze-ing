import sys
from parse import parse
from dfs import MazeGenerator
from output import write_maze


if __name__ == '__main__':
    maze_parse = parse()
    gen = MazeGenerator(maze_parse["WIDTH"], maze_parse["HEIGHT"], maze_parse.get("SEED"))
    gen.generate(maze_parse["ENTRY"][0], maze_parse["ENTRY"][1])
    write_maze(maze_parse["OUTPUT_FILE"], gen.maz.get_maze(), (maze_parse["ENTRY"][0], maze_parse["ENTRY"][1]), 
    (maze_parse["EXIT"][0], maze_parse["EXIT"][1]), "")
     