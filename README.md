Maze Solver
BCA (AI & Data Science) — PBL Project
What We're Building
For our Project-Based Learning (PBL) assignment, we are putting together a "Maze Solver"—a practical, hands-on Data Structures and Algorithms (DSA) tool. The core idea is pretty straightforward: navigate from a starting point to an endpoint in a grid without hitting any walls. We'll be coding this entirely in C, using two classic algorithms—Breadth-First Search (BFS) and Depth-First Search (DFS)—to figure out the best escape routes.
The Challenge
When you're dealing with a grid full of obstacles and dead ends, figuring out a valid path by hand is tedious. Our goal is to write a program that takes the guesswork out of this process. By applying standard graph traversal techniques, our code will systematically check different routes, avoid going in circles, and ultimately find the exit (if one actually exists).
What We Plan to Achieve
Here is a breakdown of what we are aiming to do:
Map out our maze using a standard 2D array.
Build a queue system from scratch in C to make the BFS algorithm work.
Use recursion (or a custom stack) to handle the DFS approach.
Keep a reliable record of the blocks we've already checked so the program doesn't get stuck in an infinite loop.
Trace back the final path and print it out clearly on the console.
Compare how BFS and DFS stack up against each other by looking at things like execution time, the number of nodes visited, and the length of the final path.
Tools & Technology
Language: C
Editor: Visual Studio Code
Core Data Structures: 2D Arrays, Stacks, and Queues
Core Algorithms: DFS and BFS
Version Control: Git & GitHub (to keep our code organized and collaborate without overwriting each other's work)
How It Will Work
Under the hood, the maze is just a 2D matrix where different numbers or characters represent walls, open paths, the start, and the finish line. The algorithms will check the neighboring open cells one by one. To make sure we don't accidentally check the same square twice, we'll mark them as "visited" as we go. Once the code finally hits the destination cell, it will look at the "parent" nodes it stored along the way to draw out the exact path it took to get there.
What the Final Product Will Look Like
By the end of this phase, we expect to have a fully functional console application. You'll be able to run it, see the grid, and watch the program spit out the correct path. It will also be smart enough to tell you if a maze is unsolvable. Ultimately, it’s a great way for us to prove that we understand how these DSA concepts actually work in practice, rather than just on a whiteboard.
Where We Can Take This Later
Right now it's going to be a terminal app, but down the line, we'd love to add a proper graphical interface. It would also be great to let users draw their own custom mazes, or have the program generate a random, solvable maze on its own. We might even throw in some advanced algorithms like A* (A-star) later on to make the pathfinding more efficient.# Maze-solver
BCA (AI/DS) PBL project implementing BFS and DFS for maze solving using C.
