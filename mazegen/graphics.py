from mlx import Mlx  # type: ignore[import-untyped]
from typing import Any, Optional as Opt
from collections.abc import Callable
from .mazegen import Maze
# Draws the maze, the 42, and the path using MLX42.

# Maze color selection
COLOR_WALL: int = 0xD9ADD1FF
COLOR_ENTRY: int = 0xD896CFFF
COLOR_EXIT: int = 0xCBCADCFF
COLOR_PATH: int = 0xFFD699FF

# Color palettes for key 3 cycling — each is (wall, entry, exit, path)
COLOR_P: list[tuple[int, int, int, int]] = [
    (0xD9ADD1FF, 0xD896CFFF, 0xCBCADCFF, 0xFFD699FF),  # original pink/purple
    (0x2A5298FF, 0x1E90FFFF, 0x00CED1FF, 0x87CEEBFF),  # blue ocean
    (0x2D6A4FFF, 0x52B788FF, 0x95D5B2FF, 0xD8F3DCFF),  # forest green
    (0xE76F51FF, 0xF4A261FF, 0xE9C46AFF, 0x264653FF),   # sunset orange
]


class KEY_CODES:
    KEY_ESC: int = 65307
    KEY_1: int = 65436
    KEY_2: int = 65433
    KEY_3: int = 65435
    KEY_4: int = 65430


# Handles window creation and maze rendering.
class Graphics:
    def __init__(
        self,
        maze: Maze,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path: str,
        regen_callback: Opt[Callable[[], tuple[Maze, str]]] = None
    ) -> None:
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

    # Paint entry, path, and exit cells.
    def draw_entry_exit(self) -> None:
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

    # Draw walls and fill fully closed 42 cells.
    def draw_maze(self) -> None:
        for y in range(0, self.maze.height):
            for x in range(0, self.maze.width):
                self.maze.get_cell(x, y)
                pixel_x: int = x * self.cell_size
                pixel_y: int = y * self.cell_size

                # If all four walls are closed
                # (cell == 15), draw a filled block
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

                # Otherwise draw individual walls as before
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
        hint_y: int = self.maze.height * self.cell_size + 5
        self.mlx.mlx_string_put(
                                self.mlx_ptr,
                                self.window, 5,
                                hint_y,
                                0xFFFFFFFF,
                                "1: regen; 2: path; 3: color; 4: quit"
                            )

    # Build the final image and display it.
    def key_code(self, keycode: int, _: Any) -> None:
        match keycode:
            case KEY_CODES.KEY_1:
                if self.regen_callback is not None:
                    self.maze, self.path = self.regen_callback()
                self.mlx.mlx_clear_window(self.mlx_ptr, self.window)
                self.draw_maze()
                if self.path_visible:
                    self.draw_path()
                self.draw_entry_exit()
                self.draw_hint()
            case KEY_CODES.KEY_2:
                self.path_visible = not self.path_visible
                self.mlx.mlx_clear_window(self.mlx_ptr, self.window)
                self.draw_maze()
                if self.path_visible:
                    self.draw_path()
                self.draw_entry_exit()
                self.draw_hint()
            case KEY_CODES.KEY_3:
                self.color_idx = (self.color_idx + 1) % len(COLOR_P)
                self.mlx.mlx_clear_window(self.mlx_ptr, self.window)
                self.draw_maze()
                if self.path_visible:
                    self.draw_path()
                self.draw_entry_exit()
                self.draw_hint()
            case KEY_CODES.KEY_4 | KEY_CODES.KEY_ESC:
                self.mlx.mlx_loop_exit(self.mlx_ptr)

    def render(self) -> None:
        self.draw_maze()
        self.draw_path()
        self.draw_entry_exit()
        self.draw_hint()
        self.mlx.mlx_key_hook(self.window, self.key_code, self)
        self.mlx.mlx_loop(self.mlx_ptr)
