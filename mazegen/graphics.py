# Draws the maze, the 42, and the path using MLX42.
from mlx import Mlx
from typing import Any, Optional as Opt
from collections.abc import Callable
from .mazegen import Maze

# Maze color selection
COLOR_WALL: int = 0xD9ADD1FF
COLOR_ENTRY: int = 0xD896CFFF
COLOR_EXIT: int = 0xCBCADCFF
COLOR_PATH: int = 0xFFD699FF

# Color palettes for key 3 cycling — each is (wall, entry, exit, path)
COLOR_P: list[tuple[int, int, int, int]] = [
    (0xFFD9ADD1, 0xFFD896CF, 0xFFCBCADC, 0xFFFFD699),  # original pink/purple
    (0xFF2A5298, 0xFF1E90FF, 0xFF00CED1, 0xFF87CEEB),  # blue ocean
    (0xFF2D6A4F, 0xFF52B788, 0xFF95D5B2, 0xFFD8F3DC),  # forest green
    (0xFFE76F51, 0xFFF4A261, 0xFFE9C46A, 0xFFD4847A),   # sunset orange
]


class KEY_CODES:
    """X11 keysym codes for MLX key hook and numpad equivalents."""
    KEY_ESC: int = 65307
    KEY_1: int = 65436
    NUM_1: int = 49
    KEY_2: int = 65433
    NUM_2: int = 50
    KEY_3: int = 65435
    NUM_3: int = 51
    KEY_4: int = 65430
    NUM_4: int = 52


class Graphics:
    """Handles MLX window creation and maze rendering.

    Args:
        maze: The maze object to display.
        entry: Entry cell coordinates (x, y).
        exit_pos: Exit cell coordinates (x, y).
        path: Solution path string using N/S/E/W characters.
        regen_callback:
        Optional callable that returns a new (maze, path) tuple.
    """
    def __init__(
        self,
        maze: Maze,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path: str,
        regen_callback: Opt[Callable[[], tuple[Maze, str]]] = None
    ) -> None:
        """Initialize the Graphics object and create the MLX window."""
        self.mlx: Mlx = None
        self.mlx_ptr: Any = None
        self.maze: Maze = maze
        self.entry: tuple[int, int] = entry
        self.exit_pos: tuple[int, int] = exit_pos
        self.path: str = path
        self.regen_callback: Opt[
            Callable[
                [],
                tuple[
                    Maze,
                    str
                ]
            ]
        ] = regen_callback
        self.cell_size: int = 20
        self.path_visible: bool = True
        self.color_idx: int = 0
        self.window: Any = None
        self.image: Any = None
        try:
            self.mlx = Mlx()
            self.window_width = self.maze.width * self.cell_size + 1
            self.window_height = (self.maze.height + 5) * self.cell_size + 1
            self.mlx_ptr = self.mlx.mlx_init()
            self.window = self.mlx.mlx_new_window(
                                                self.mlx_ptr,
                                                self.window_width,
                                                self.window_height,
                                                "A-Maze-ing"
                                            )
            self.image = self.mlx.mlx_new_image(
                                                self.mlx_ptr,
                                                self.window_width,
                                                self.window_height
                                            )
        except IOError as e:
            print("ERROR - Unable to create window", e)

    def draw_entry_exit(self) -> None:
        """Draw the entry and exit cells in their palette colors."""
        entry_x: int = self.entry[0] * self.cell_size
        entry_y: int = self.entry[1] * self.cell_size
        for screen_x in range(entry_x, entry_x + self.cell_size):
            for screen_y in range(entry_y, entry_y + self.cell_size):
                self.mlx.mlx_pixel_put(
                                    self.mlx_ptr,
                                    self.window,
                                    screen_x, screen_y,
                                    COLOR_P[self.color_idx][1]
                                )
        exit_x: int = self.exit_pos[0] * self.cell_size
        exit_y: int = self.exit_pos[1] * self.cell_size
        for screen_x in range(exit_x, exit_x + self.cell_size):
            for screen_y in range(exit_y, exit_y + self.cell_size):
                self.mlx.mlx_pixel_put(
                                    self.mlx_ptr,
                                    self.window, screen_x,
                                    screen_y,
                                    COLOR_P[self.color_idx][2])

    def draw_path(self) -> None:
        """Draw the solution path cells in the current palette path color."""
        current_x: int = self.entry[0]
        current_y: int = self.entry[1]
        for direction in self.path:
            if direction == 'N':
                current_y = current_y - 1
            if direction == 'S':
                current_y = current_y + 1
            if direction == 'E':
                current_x = current_x + 1
            if direction == 'W':
                current_x = current_x - 1
            if (
                0 <= current_x < self.maze.width and
                0 <= current_y < self.maze.height
            ):
                pixel_x: int = current_x * self.cell_size
                pixel_y: int = current_y * self.cell_size
                for screen_x in range(pixel_x, pixel_x + self.cell_size):
                    for screen_y in range(pixel_y, pixel_y + self.cell_size):
                        self.mlx.mlx_pixel_put(
                            self.mlx_ptr, self.window,
                            screen_x, screen_y,
                            COLOR_P[self.color_idx][3]
                        )

    def draw_maze(self) -> None:
        """Draw all maze walls and filled cells including the 42 pattern."""
        for y in range(0, self.maze.height):
            for x in range(0, self.maze.width):
                self.maze.get_cell(x, y)
                pixel_x: int = x * self.cell_size
                pixel_y: int = y * self.cell_size

                """If all four walls are closed (cell == 15),
                draw a filled block"""
                cell: int = self.maze.get_cell(x, y)
                if cell == 15:
                    for screen_x in range(pixel_x, pixel_x + self.cell_size):
                        for screen_y in range(
                                            pixel_y,
                                            pixel_y + self.cell_size):
                            self.mlx.mlx_pixel_put(
                                                    self.mlx_ptr,
                                                    self.window, screen_x,
                                                    screen_y,
                                                    COLOR_P[self.color_idx][0]
                                                )
                    continue

                """Otherwise draw individual walls as before"""
                if self.maze.has_wall(x, y, 0):
                    for screen_x in range(pixel_x, pixel_x + self.cell_size):
                        self.mlx.mlx_pixel_put(
                                            self.mlx_ptr,
                                            self.window, screen_x,
                                            pixel_y,
                                            COLOR_P[self.color_idx][0]
                                        )
                if self.maze.has_wall(x, y, 1):
                    for screen_y in range(pixel_y, pixel_y + self.cell_size):
                        self.mlx.mlx_pixel_put(
                                            self.mlx_ptr,
                                            self.window,
                                            pixel_x + self.cell_size,
                                            screen_y,
                                            COLOR_P[self.color_idx][0]
                                        )
                if self.maze.has_wall(x, y, 2):
                    for screen_x in range(pixel_x, pixel_x + self.cell_size):
                        self.mlx.mlx_pixel_put(
                                            self.mlx_ptr,
                                            self.window,
                                            screen_x,
                                            pixel_y + self.cell_size,
                                            COLOR_P[self.color_idx][0]
                                        )
                if self.maze.has_wall(x, y, 3):
                    for screen_y in range(pixel_y, pixel_y + self.cell_size):
                        self.mlx.mlx_pixel_put(
                                                self.mlx_ptr,
                                                self.window,
                                                pixel_x,
                                                screen_y,
                                                COLOR_P[self.color_idx][0]
                                            )

    def draw_hint(self) -> None:
        """Draw the key hint text at the bottom of the window."""
        hint_y: int = self.maze.height * self.cell_size + 5
        self.mlx.mlx_string_put(
                                self.mlx_ptr,
                                self.window, 5,
                                hint_y,
                                0xFFFFFFFF,
                                "1: regen; 2: path; 3: color; 4: quit"
                            )

    def key_code(self, keycode: int, _: Any) -> None:
        """Handle key press events from the MLX key hook.

        Args:
            keycode: The X11 keysym code of the pressed key.
            _: Unused param passed by mlx_key_hook.
        """
        match keycode:
            case KEY_CODES.KEY_1 | KEY_CODES.NUM_1:
                if self.regen_callback is not None:
                    self.maze, self.path = self.regen_callback()
                self.mlx.mlx_clear_window(self.mlx_ptr, self.window)
                if self.path_visible:
                    self.draw_path()
                self.draw_entry_exit()
                self.draw_maze()
                self.draw_hint()
            case KEY_CODES.KEY_2 | KEY_CODES.NUM_2:
                self.path_visible = not self.path_visible
                self.mlx.mlx_clear_window(self.mlx_ptr, self.window)
                if self.path_visible:
                    self.draw_path()
                self.draw_entry_exit()
                self.draw_maze()
                self.draw_hint()
            case KEY_CODES.KEY_3 | KEY_CODES.NUM_3:
                self.color_idx = (self.color_idx + 1) % len(COLOR_P)
                self.mlx.mlx_clear_window(self.mlx_ptr, self.window)
                if self.path_visible:
                    self.draw_path()
                self.draw_entry_exit()
                self.draw_maze()
                self.draw_hint()
            case KEY_CODES.KEY_4 | KEY_CODES.NUM_4 | KEY_CODES.KEY_ESC:
                self.mlx.mlx_loop_exit(self.mlx_ptr)

    def render(self) -> None:
        """Render the maze and start the MLX event loop."""
        self.draw_path()
        self.draw_entry_exit()
        self.draw_maze()
        self.draw_hint()
        self.mlx.mlx_hook(self.window, 33, 0,
                          self.mlx.mlx_loop_exit, self.mlx_ptr)
        self.mlx.mlx_key_hook(self.window, self.key_code, self)
        self.mlx.mlx_loop(self.mlx_ptr)
