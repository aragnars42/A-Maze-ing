# Draws the maze, the 42, and the path using MLX42.

import sys
import os, sys
sys.path.insert(0, os.path.expanduser("~/MLX42/ffi/python"))
from libmlx import *
from typing import List, Tuple
from mazegen.mazegen import Maze

# Maze color selection
COLOR_WALL = 0xD9ADD1FF
COLOR_ENTRY = 0xD896CFFF
COLOR_EXIT = 0xCBCADCFF
COLOR_PATH = 0xFFD699FF


# Handles window creation and maze rendering.
class Graphics:
	def __init__(self, maze, entry: Tuple[int, int], exit_pos: Tuple[int, int], path: str):
		self.maze = maze
		self.entry = entry
		self.exit_pos = exit_pos
		self.path = path
		self.cell_size = 20
		self.window = None
		self.image = None
		try:
			self.window_width = self.maze.width * self.cell_size
			self.window_height = self.maze.height * self.cell_size
			self.window = mlx.mlx_init(self.window_width, self.window_height, b"A-Maze-ing", True)
			self.image = mlx.mlx_new_image(self.window, self.window_width, self.window_height)
		except IOError as e:
			print("ERROR - Unable to create window", e)

    # Paint entry, path, and exit cells.
	def draw_entry_exit_path(self) -> None:
		entry_x = self.entry[0] * self.cell_size
		entry_y = self.entry[1] * self.cell_size
		for screen_x in range(entry_x, entry_x + self.cell_size):
			for screen_y in range(entry_y, entry_y + self.cell_size):
				mlx.mlx_put_pixel(self.image, screen_x, screen_y, COLOR_ENTRY)
		current_x = self.entry[0]
		current_y = self.entry[1]
		for direction in self.path:
			if direction == 'N':
				current_y = current_y - 1
			if direction == 'S':
				current_y = current_y + 1
			if direction == 'E':
				current_x = current_x + 1
			if direction == 'W':
				current_x = current_x - 1
			if 0 <= current_x < self.maze.width and 0 <= current_y < self.maze.height:
				pixel_x = current_x * self.cell_size
				pixel_y = current_y * self.cell_size
				for screen_x in range(pixel_x, pixel_x + self.cell_size):
					for screen_y in range(pixel_y, pixel_y + self.cell_size):
						mlx.mlx_put_pixel(self.image, screen_x, screen_y, COLOR_PATH)
		exit_x = self.exit_pos[0] * self.cell_size
		exit_y = self.exit_pos[1] * self.cell_size
		for screen_x in range(exit_x, exit_x + self.cell_size):
			for screen_y in range(exit_y, exit_y + self.cell_size):
				mlx.mlx_put_pixel(self.image, screen_x, screen_y, COLOR_EXIT)

    # Draw walls and fill fully closed 42 cells.
	def draw_maze(self) -> None:
		for y in range(0, self.maze.height):
			for x in range(0, self.maze.width):
				self.maze.get_cell(x, y)
				pixel_x = x * self.cell_size
				pixel_y = y * self.cell_size

                # If all four walls are closed (cell == 15), draw a filled block
				cell = self.maze.get_cell(x, y)
				if cell == 15:
					for screen_x in range(pixel_x, pixel_x + self.cell_size):
						for screen_y in range(pixel_y, pixel_y + self.cell_size):
							mlx.mlx_put_pixel(self.image, screen_x, screen_y, COLOR_WALL)
					continue

                # Otherwise draw individual walls as before
				if self.maze.has_wall(x, y, 0):
					for screen_x in range(pixel_x, pixel_x + self.cell_size):
						mlx.mlx_put_pixel(self.image, screen_x, pixel_y, COLOR_WALL)
				if self.maze.has_wall(x, y, 1):
					for screen_y in range(pixel_y, pixel_y + self.cell_size):
						mlx.mlx_put_pixel(self.image, pixel_x + self.cell_size, screen_y, COLOR_WALL)
				if self.maze.has_wall(x, y, 2):
					for screen_x in range(pixel_x, pixel_x + self.cell_size):
						mlx.mlx_put_pixel(self.image, screen_x, pixel_y + self.cell_size, COLOR_WALL)
				if self.maze.has_wall(x, y, 3):
					for screen_y in range(pixel_y, pixel_y + self.cell_size):
						mlx.mlx_put_pixel(self.image, pixel_x, screen_y, COLOR_WALL)

    # Build the final image and display it.
	def render(self) -> None:
		self.image = mlx.mlx_new_image(self.window, self.window_width, self.window_height)
		self.draw_entry_exit_path()
		self.draw_maze()
		mlx.mlx_image_to_window(self.window, self.image, 0, 0)
		mlx.mlx_loop(self.window)
