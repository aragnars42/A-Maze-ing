*This project has been created as part of the 42 curriculum by aragnars, tmontezu.*

---

# A-Maze-ing

A Python-based maze generation and visualization system using Depth-First Search (DFS) algorithm for maze generation, with graphical rendering, shortest-path finding, and the iconic 42 logo displayed at the center of every maze.

---

## Description

A-Maze-ing is a maze generation program that creates random rectangular mazes and displays them graphically using MLX42. The program generates a perfect (or imperfect) maze using DFS, identifies the shortest path from entry to exit using BFS, and renders the result with color-coded visualization (entry, exit, path, and walls). A signature 42 logo is drawn at the center of each generated maze. 

---

## Instructions

### Requirements

- Python 3.10 or higher
- MLX42 library (minilibx Python wrapper)
- cmake (for building MLX42)
- A C compiler (gcc or clang)

### Installation & Setup

**1. Clone the repository:**
```bash
git clone <repo-url>
cd A-Maze-ing
```

**2. Install dependencies:**
```bash
make install
```

This will:
- Create a Python virtual environment
- Install the MLX42 Python wheel
- Install required Python packages from `requirements.txt`

### Usage

**Run with default configuration:**
```bash
make run
```

**Run with custom configuration file:**
```bash
python3 a_maze_ing.py <config_file>
```

Example:
```bash
python3 a_maze_ing.py config.txt
```

**Debug mode:**
```bash
make debug
```

**Linting and type checking:**
```bash
make lint         # Run flake8 and mypy
make lint-strict  # Run mypy in strict mode
```

**Clean build artifacts:**
```bash
make clean
```

---

## Configuration File

The configuration file uses a simple `KEY=VALUE` format. Lines starting with `#` are comments and ignored.

### Required Fields

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `WIDTH` | int | Maze width in cells (must be > 0) | `20` |
| `HEIGHT` | int | Maze height in cells (must be > 0) | `30` |
| `ENTRY` | x,y | Starting position (format: `x,y`) | `0,0` |
| `EXIT` | x,y | Ending position (format: `x,y`) | `19,14` |
| `OUTPUT_FILE` | string | Path where maze will be saved (hex format) | `maze.txt` |
| `PERFECT` | bool | Perfect maze with single solution (`True` or `False`) | `False` |

### Example Configuration

```
# Maze generation config
WIDTH=20
HEIGHT=30
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
```

### Validation

Syntax rules:
- All required keys need to be present
- Width and height should be positive
- Entry and exit should be within bounds
- Entry and exit should not be the same position
- Coordinates should be valid integers

---

## Maze Generation Algorithm

### Depth-First Search (DFS)

**What we chose:** Depth-First Search (DFS) is a search algorithm that starts at a specific node and explores as much as possible along all the nodes before (neighbors) backtracking when there are no more moves available.

**Algorithm :**
1. Start at entry position and mark as visited.
2. Randomly choose an unvisited neighbor.
3. Open the wall between current cell and neighbor.
4. Move to the neighbor.
5. If no unvisited neighbors exist, backtrack.
6. Repeat until there is nowhere to backtrack to (maze entry).

---

## Path Finding

**Algorithm:** Breadth-First Search (BFS)

We use BFS (Breadth-First Search) to find the shortest path, creating two variables: `start: entry` and `end: exit`, which iterate through and create a list with this shortest path.
BFS finds the shortest path because it explores all paths in ascending order of distance from the start.


---

## Reusable Components

### `mazegen/` Module

The `mazegen` folder contains reusable, independent modules:

#### **`mazegen/mazegen.py` – Maze Data Structure**
- **Purpose:** Core maze representation using hexadecimal wall encoding.

#### **`mazegen/dfs.py` – Maze Generator**
- **Purpose:** Generates perfect mazes using DFS.

#### **`mazegen/bfs.py` – Path Finder**
- **Purpose:** Finds shortest path from entry to exit.

#### **`mazegen/parse.py` – Configuration Parser**
- **Purpose:** Parses and validates configuration files.

#### **`mazegen/output.py` – File Export**
- **Purpose:** Exports maze and solution to file in hex format.

#### **`mazegen/graphics.py` – Visualization**
- **Purpose:** Renders maze using MLX42 graphics library.

---

## Advanced Features

### 42 Logo Integration

Every generated maze displays the iconic "42" logo at its center:
- Logo cells have all four walls closed (hex value 15), rendering as solid blocks.
- Drawn after maze generation and wall normalization.
- Path finding automatically routes around the logo.

### User interaction

The user has four differnt options to interact with the program:
1. Regenerate the maze.
2. Show/hide the path.
3. Change the colorway.
4. Quit the program.

---

## Team and Project Management

### Team Members and Roles

| Member | Login | Role |
|--------|-------|------|
| Thaynara Montezuma | tmontezu | Parser, path finding (BFS), Maze generation (DFS) 
| Andrea Nordquist Ragnarsdottir | aragnars | logo integration, debugging, graphics rendering |

### Planning and Evolution

**Initial approach:**
- Divided tasks by module: one person focused on generation/logic, the other on parsing/output/graphics.
- Each worked independently on their assigned components.

**Mid-project adjustments:**
- Discovered import structure needed refactoring to make `mazegen` properly modular.
- Moved all game logic into the `mazegen/` package for clarity and reusability.
- Collaborated on path-finding integration to ensure the path avoids the 42 logo.

**Final integration:**
- Merged all components into a cohesive system.
- Implemented regeneration loop to guarantee valid paths that don't intersect the logo.

### What Worked Well

- **Clear module boundaries** made it easy to test components independently.
- **Configuration-driven approach** allowed flexible testing without code changes.
- **DFS + BFS combination** is efficient and produces high-quality mazes.
- **Modular `mazegen` package** makes components reusable in other projects.

### areas for Improvement

- **Performance:** Could optimize rendering with batching instead of per-pixel updates.
- **Algorithm choice:** Could add Prim's algorithm as an option for stylistically different mazes.

### Tools Used

- **Git** – Version control and collaboration.
- **Make** – Build automation, environment setup, and task management.
- **Python 3.10+** – Language choice for cross-platform compatibility.
- **MLX42** – Graphics library for window rendering.
- **flake8** – Code style checking.
- **mypy** – Static type checking.
- **cmake** – Build system for MLX42 C library.

---

## Resources

### Documentation
- [MLX42 Official Documentation](https://github.com/42Paris/MLX42)
- [Python 3.10 Docs](https://docs.python.org/3.10/)
- [Type Hints in Python (PEP 484)](https://www.python.org/dev/peps/pep-0484/)

### Algorithm References
- [Depth-First Search – Jamis Buck's Blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-depth-first-search)
- [Breadth-First Search – GeeksforGeeks](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)
- [Maze Generation Algorithms Visualization (YouTube)](https://www.youtube.com/watch?v=uctN47p_KVk)

### AI Usage

AI tools were used in this project for:
- **Debugging:** Identifying import path issues for the mlx wrapper and thread safety.
- **Learning:** Understanding MLX42 API patterns and Python best practices.

**AI was NOT used for:**
- Core algorithm implementations (DFS, BFS).
- Project architecture or design decisions.
- Configuration parsing or validation logic.

---
