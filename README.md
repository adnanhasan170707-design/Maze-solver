# Maze Solver — Phase II (C + Python Tkinter GUI)

BCA (AI & DS) PBL project: maze pathfinding using BFS and DFS.

## Features
- Maze represented as a 2D grid in C.
- BFS uses a queue; DFS uses a stack.
- Visited-cell tracking and parent-based path reconstruction.
- GUI buttons for BFS, DFS, Run Both, Reset View, and a visited-cell toggle.
- Displays path length, nodes visited, and execution time.
- Python is used only for the graphical interface; the pathfinding algorithms remain in C.

## Requirements
- macOS with Python 3, Tkinter, and Xcode Command Line Tools (`clang`).
- If compiler tools are missing, run `xcode-select --install` in Terminal.
- Check Tkinter availability with `python3 -m tkinter`.

## Run the GUI
Open this folder in VS Code, then run in the integrated terminal:

```bash
python3 frontend.py
```

The GUI compiles `maze_solver.c` automatically when needed.

## Run the C backend directly

```bash
clang -std=c11 -Wall -Wextra maze_solver.c -o maze_solver
./maze_solver bfs
./maze_solver dfs
```

The backend outputs JSON for the GUI to read.

## Team
Team Falcon — BCA (AI & DS)
- Adnan, Hasan — Team Lead
- Chauhan, Aditya
- Kurmanchali, Udit

## Important
This is an initial integrated version. Run it on your own Mac, verify the GUI and test cases, and record actual outputs/screenshots before marking tasks as completed in the progress report.
