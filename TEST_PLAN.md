# Test Plan

Record actual outcomes after running on your Mac.

| ID | Test | Expected result | Status |
|---|---|---|---|
| T1 | Run BFS from GUI | Path and metrics displayed | Pending local verification |
| T2 | Run DFS from GUI | Path and metrics displayed | Pending local verification |
| T3 | Run Both | BFS/DFS metrics shown for comparison | Pending local verification |
| T4 | Reset View | Path and visited overlays cleared | Pending local verification |
| T5 | Toggle visited cells | Visited overlay can be hidden/shown | Pending local verification |
| T6 | Compile C with warnings enabled | No compile errors or warnings | Pending local verification |

BFS should find a shortest path for this unweighted maze. Execution times vary between runs; do not claim one algorithm is generally faster based on a single run. This version uses a fixed maze; user-editable mazes are future scope.
