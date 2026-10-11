
import json
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "maze_solver.c"
BINARY = HERE / "maze_solver"


class MazeGUI:
    def __init__(self, root):
        self.root = root
        root.title("Maze Solver | BFS & DFS")
        root.geometry("1000x650")
        root.minsize(800, 550)

        self.maze = []
        self.path = set()
        self.visited = set()
        self.bfs_path = set()
        self.dfs_path = set()
        self.bfs_result = None
        self.dfs_result = None
        self.display_both = False

        self.show_visited = tk.BooleanVar(value=True)

        # Header
        header = tk.Frame(
            root, bg="#14213d", padx=18, pady=13
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="MAZE SOLVER",
            bg="#14213d",
            fg="white",
            font=("Arial", 20, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="C Algorithms • BFS (Queue) • DFS (Stack)",
            bg="#14213d",
            fg="#dbeafe",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(3, 0))

        # Buttons
        controls = tk.Frame(root, padx=14, pady=10)
        controls.pack(fill="x")

        tk.Button(
            controls,
            text="Run BFS (Queue)",
            command=lambda: self.run_one("bfs"),
            bg="#2563eb",
            fg="white",
            padx=10,
            pady=7
        ).pack(side="left", padx=(0, 7))

        tk.Button(
            controls,
            text="Run DFS (Stack)",
            command=lambda: self.run_one("dfs"),
            bg="#7042bf",
            fg="white",
            padx=10,
            pady=7
        ).pack(side="left", padx=(0, 7))

        tk.Button(
            controls,
            text="Run Both",
            command=self.run_both,
            bg="#374151",
            fg="white",
            padx=10,
            pady=7
        ).pack(side="left", padx=(0, 7))

        tk.Button(
            controls,
            text="Reset View",
            command=self.reset,
            padx=10,
            pady=7
        ).pack(side="left", padx=(0, 7))

        tk.Checkbutton(
            controls,
            text="Show visited cells",
            variable=self.show_visited,
            command=self.redraw
        ).pack(side="left")

        # Main maze canvas
        body = tk.Frame(root, padx=14, pady=4)
        body.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            body,
            bg="#f8fafc",
            highlightthickness=1,
            highlightbackground="#cbd5e1"
        )
        self.canvas.pack(
            side="left", fill="both", expand=True
        )

        # Results panel
        side = tk.Frame(body, width=240, padx=14, pady=10)
        side.pack(side="right", fill="y")
        side.pack_propagate(False)

        tk.Label(
            side,
            text="RESULTS",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 8))

        self.result = tk.StringVar(
            value="Choose BFS, DFS, or Run Both."
        )

        tk.Label(
            side,
            textvariable=self.result,
            justify="left",
            anchor="nw",
            wraplength=215,
            font=("Arial", 10)
        ).pack(fill="x", anchor="w")

        tk.Label(
            side,
            text="LEGEND",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(20, 8))

        legend = [
            ("#1f2937", "Wall"),
            ("#ffffff", "Open cell"),
            ("#93c5fd", "Visited"),
            ("#22c55e", "BFS path"),
            ("#a78bfa", "DFS path"),
            ("#f59e0b", "Start / shared path"),
            ("#ef4444", "Target")
        ]

        for color, label in legend:
            line = tk.Frame(side)
            line.pack(anchor="w", pady=2)

            tk.Label(
                line,
                bg=color,
                width=2,
                relief="solid",
                bd=1
            ).pack(side="left", padx=(0, 7))

            tk.Label(
                line, text=label
            ).pack(side="left")

        # Status bar
        self.status = tk.StringVar(value="Ready")

        tk.Label(
            root,
            textvariable=self.status,
            anchor="w",
            relief="sunken",
            padx=10,
            pady=5
        ).pack(fill="x", side="bottom")

        self.load_maze()
        root.bind("<Configure>", self.on_resize)

    # Compile C backend when needed
    def compile_backend(self):
        if not SOURCE.exists():
            raise FileNotFoundError(
                f"C source file not found:\n{SOURCE}"
            )

        needs_compile = (
            not BINARY.exists()
            or BINARY.stat().st_mtime < SOURCE.stat().st_mtime
        )

        if needs_compile:
            compiler = (
                "clang"
                if sys.platform == "darwin"
                else "gcc"
            )

            try:
                result = subprocess.run(
                    [
                        compiler,
                        "-std=c11",
                        "-Wall",
                        "-Wextra",
                        str(SOURCE),
                        "-o",
                        str(BINARY)
                    ],
                    capture_output=True,
                    text=True
                )
            except FileNotFoundError:
                raise RuntimeError(
                    f"{compiler} not found. On macOS, run:\n"
                    "xcode-select --install"
                )

            if result.returncode != 0:
                raise RuntimeError(
                    result.stderr or "C compilation failed."
                )

        return str(BINARY)

    # Execute C program and read its JSON output
    def get_result(self, algorithm):
        binary = self.compile_backend()

        result = subprocess.run(
            [binary, algorithm],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr or "C backend failed."
            )

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            raise RuntimeError(
                "C backend did not return valid JSON.\n"
                + result.stdout
            )

        required = {
            "maze", "path", "visited", "found",
            "moves", "nodes_visited", "seconds"
        }

        missing = required.difference(data.keys())

        if missing:
            raise RuntimeError(
                "Missing JSON fields from C backend: "
                + ", ".join(sorted(missing))
            )

        return data

    # Load initial maze
    def load_maze(self):
        try:
            data = self.get_result("bfs")
            self.maze = data["maze"]
            self.redraw()
            self.status.set("Maze loaded successfully")

        except Exception as exc:
            messagebox.showerror("Startup error", str(exc))
            self.status.set("Could not load C backend")

    # Run only BFS or DFS
    def run_one(self, algorithm):
        try:
            data = self.get_result(algorithm)

            self.maze = data["maze"]
            self.display_both = False

            self.path = {
                tuple(p) for p in data["path"]
            }
            self.visited = {
                tuple(p) for p in data["visited"]
            }

            self.redraw()

            if data["found"]:
                self.result.set(
                    f"{algorithm.upper()} — Path found\n\n"
                    f"Path length: {data['moves']} moves\n"
                    f"Nodes visited: {data['nodes_visited']}\n"
                    f"Execution time: "
                    f"{data['seconds']:.9f} seconds"
                )
                self.status.set(
                    f"{algorithm.upper()} completed"
                )
            else:
                self.result.set(
                    f"{algorithm.upper()} — No path exists"
                )
                self.status.set(
                    "Destination is unreachable"
                )

        except Exception as exc:
            messagebox.showerror("Run error", str(exc))
            self.status.set("Algorithm execution failed")

    # Run both algorithms on the same maze
    def run_both(self):
        try:
            self.status.set("Running BFS and DFS...")
            self.root.update_idletasks()

            bfs = self.get_result("bfs")
            dfs = self.get_result("dfs")

            self.bfs_result = bfs
            self.dfs_result = dfs

            self.maze = bfs["maze"]

            self.bfs_path = {
                tuple(p) for p in bfs["path"]
            }
            self.dfs_path = {
                tuple(p) for p in dfs["path"]
            }

            self.visited = (
                {tuple(p) for p in bfs["visited"]}
                | {tuple(p) for p in dfs["visited"]}
            )

            self.display_both = True
            self.path = set()

            self.redraw()

            bfs_moves = (
                f"{bfs['moves']} moves"
                if bfs["found"] else "No path"
            )
            dfs_moves = (
                f"{dfs['moves']} moves"
                if dfs["found"] else "No path"
            )

            self.result.set(
                "BFS vs DFS COMPARISON\n\n"
                f"BFS (Queue)\n"
                f"Path: {bfs_moves}\n"
                f"Nodes visited: {bfs['nodes_visited']}\n"
                f"Time: {bfs['seconds']:.9f} sec\n\n"
                f"DFS (Stack)\n"
                f"Path: {dfs_moves}\n"
                f"Nodes visited: {dfs['nodes_visited']}\n"
                f"Time: {dfs['seconds']:.9f} sec\n\n"
                "Both paths shown on the maze."
            )

            self.status.set(
                "BFS and DFS paths displayed"
            )

        except Exception as exc:
            messagebox.showerror(
                "Comparison error", str(exc)
            )
            self.status.set("Comparison failed")

    # Reset displayed paths
    def reset(self):
        self.path = set()
        self.visited = set()
        self.bfs_path = set()
        self.dfs_path = set()
        self.display_both = False
        self.bfs_result = None
        self.dfs_result = None

        self.result.set(
            "View reset. Choose an algorithm to solve the maze."
        )

        self.redraw()
        self.status.set("View reset")

    # Redraw according to the current display mode
    def redraw(self):
        if not self.maze:
            return

        if self.display_both:
            self.draw_both()
        else:
            self.draw()

    # Draw one algorithm's path
    def draw(self):
        self.canvas.delete("all")

        if not self.maze:
            return

        rows = len(self.maze)
        cols = len(self.maze[0])

        width = max(1, self.canvas.winfo_width())
        height = max(1, self.canvas.winfo_height())

        cell = max(
            1,
            min(
                28,
                (width - 24) // cols,
                (height - 24) // rows
            )
        )

        x0 = max(10, (width - cols * cell) // 2)
        y0 = max(10, (height - rows * cell) // 2)

        for r, line in enumerate(self.maze):
            for c, ch in enumerate(line):
                p = (r, c)

                if ch == "#":
                    color = "#1f2937"
                elif ch == "S":
                    color = "#f59e0b"
                elif ch == "T":
                    color = "#ef4444"
                elif p in self.path:
                    color = "#22c55e"
                elif (
                    self.show_visited.get()
                    and p in self.visited
                ):
                    color = "#93c5fd"
                else:
                    color = "#ffffff"

                self.draw_cell(
                    r, c, cell, x0, y0, color, ch
                )

    # Draw both paths on the same maze
    def draw_both(self):
        self.canvas.delete("all")

        if not self.maze:
            return

        rows = len(self.maze)
        cols = len(self.maze[0])

        width = max(1, self.canvas.winfo_width())
        height = max(1, self.canvas.winfo_height())

        cell = max(
            1,
            min(
                28,
                (width - 24) // cols,
                (height - 24) // rows
            )
        )

        x0 = max(10, (width - cols * cell) // 2)
        y0 = max(10, (height - rows * cell) // 2)

        for r, line in enumerate(self.maze):
            for c, ch in enumerate(line):
                p = (r, c)

                if ch == "#":
                    color = "#1f2937"
                elif ch == "S":
                    color = "#f59e0b"
                elif ch == "T":
                    color = "#ef4444"
                elif (
                    p in self.bfs_path
                    and p in self.dfs_path
                ):
                    # Shared by both final paths
                    color = "#f59e0b"
                elif p in self.bfs_path:
                    color = "#22c55e"
                elif p in self.dfs_path:
                    color = "#a78bfa"
                elif (
                    self.show_visited.get()
                    and p in self.visited
                ):
                    color = "#93c5fd"
                else:
                    color = "#ffffff"

                self.draw_cell(
                    r, c, cell, x0, y0, color, ch
                )

    # Common cell-drawing helper
    def draw_cell(self, r, c, cell, x0, y0, color, ch):
        x1 = x0 + c * cell
        y1 = y0 + r * cell
        x2 = x1 + cell
        y2 = y1 + cell

        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            outline="#cbd5e1"
        )

        if ch in "ST":
            self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=ch,
                fill="white",
                font=(
                    "Arial",
                    max(9, cell // 2),
                    "bold"
                )
            )

    # Redraw after window resizing
    def on_resize(self, event):
        if event.widget == self.root:
            self.redraw()


if __name__ == "__main__":
    window = tk.Tk()
    app = MazeGUI(window)
    window.mainloop()
