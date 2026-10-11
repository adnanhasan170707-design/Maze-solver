#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define ROWS 11
#define COLS 21
#define MAX_CELLS (ROWS * COLS)
typedef struct { int r, c; } Point;

static const char *template_maze[ROWS] = {
    "#####################",
    "#S....#.............#",
    "#.##..#.#####.###...#",
    "#.##..#.....#...#...#",
    "#....#####..#...###.#",
    "####.####...#.......#",
    "#....#......#####...#",
    "#.##.#.####.....#...#",
    "#.##....#...###.#...#",
    "#..................T#",
    "#####################"
};
static const int dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};
static char maze[ROWS][COLS + 1];
static int visited[ROWS][COLS];
static Point parent_cell[ROWS][COLS], start_point, target_point, path[MAX_CELLS];
static int path_count, nodes_visited, found;

static int same(Point a, Point b) { return a.r == b.r && a.c == b.c; }
static int valid(int r, int c) { return r >= 0 && r < ROWS && c >= 0 && c < COLS && maze[r][c] != '#'; }
static void initialize(void) {
    path_count = nodes_visited = found = 0;
    for (int r = 0; r < ROWS; r++) {
        strcpy(maze[r], template_maze[r]);
        for (int c = 0; c < COLS; c++) {
            visited[r][c] = 0;
            parent_cell[r][c] = (Point){-1, -1};
            if (maze[r][c] == 'S') start_point = (Point){r, c};
            if (maze[r][c] == 'T') target_point = (Point){r, c};
        }
    }
}
static void reconstruct(void) {
    Point reverse_path[MAX_CELLS]; int count = 0; Point p = target_point;
    while (!same(p, start_point) && count < MAX_CELLS) {
        reverse_path[count++] = p;
        Point previous = parent_cell[p.r][p.c];
        if (previous.r < 0 || previous.c < 0) { count = 0; break; }
        p = previous;
    }
    if (same(p, start_point)) {
        reverse_path[count++] = start_point; path_count = count;
        for (int i = 0; i < count; i++) path[i] = reverse_path[count - i - 1];
    }
}
static void bfs(void) {
    Point q[MAX_CELLS]; int front = 0, back = 0;
    q[back++] = start_point; visited[start_point.r][start_point.c] = 1;
    while (front < back) {
        Point p = q[front++]; nodes_visited++;
        if (same(p, target_point)) { found = 1; break; }
        for (int i = 0; i < 4; i++) {
            int nr = p.r + dr[i], nc = p.c + dc[i];
            if (valid(nr, nc) && !visited[nr][nc]) {
                visited[nr][nc] = 1; parent_cell[nr][nc] = p; q[back++] = (Point){nr, nc};
            }
        }
    }
    if (found) reconstruct();
}
static void dfs(void) {
    Point stack[MAX_CELLS]; int top = 0;
    stack[top++] = start_point; visited[start_point.r][start_point.c] = 1;
    while (top > 0) {
        Point p = stack[--top]; nodes_visited++;
        if (same(p, target_point)) { found = 1; break; }
        for (int i = 3; i >= 0; i--) {
            int nr = p.r + dr[i], nc = p.c + dc[i];
            if (valid(nr, nc) && !visited[nr][nc]) {
                visited[nr][nc] = 1; parent_cell[nr][nc] = p; stack[top++] = (Point){nr, nc};
            }
        }
    }
    if (found) reconstruct();
}
static void print_points(Point *points, int count) {
    putchar('[');
    for (int i = 0; i < count; i++) { if (i) putchar(','); printf("[%d,%d]", points[i].r, points[i].c); }
    putchar(']');
}
int main(int argc, char **argv) {
    if (argc != 2 || (strcmp(argv[1], "bfs") && strcmp(argv[1], "dfs"))) {
        fprintf(stderr, "Usage: %s bfs|dfs\n", argv[0]); return 2;
    }
    initialize(); clock_t begin = clock();
    if (!strcmp(argv[1], "bfs")) bfs(); else dfs();
    double seconds = (double)(clock() - begin) / CLOCKS_PER_SEC;
    printf("{\"algorithm\":\"%s\",\"found\":%s,\"rows\":%d,\"cols\":%d,\"moves\":%d,\"nodes_visited\":%d,\"seconds\":%.9f,\"visited\":", argv[1], found ? "true" : "false", ROWS, COLS, found ? path_count - 1 : 0, nodes_visited, seconds);
    Point visited_points[MAX_CELLS]; int count = 0;
    for (int r = 0; r < ROWS; r++) for (int c = 0; c < COLS; c++) if (visited[r][c]) visited_points[count++] = (Point){r,c};
    print_points(visited_points, count); printf(",\"path\":"); print_points(path, path_count);
    printf(",\"maze\":[");
    for (int r = 0; r < ROWS; r++) { if (r) putchar(','); printf("\"%s\"", maze[r]); }
    printf("]}\n"); return 0;
}
