import random
import heapq
import tkinter as tk

def generate_maze(width, height):
    maze = [['#' for _ in range(width)] for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = ' '

    while stack:
        x, y = stack[-1]
        neighbors = []

        if x > 1 and maze[y][x - 2] == '#':
            neighbors.append((x - 2, y))
        if x < width - 2 and maze[y][x + 2] == '#':
            neighbors.append((x + 2, y))
        if y > 1 and maze[y - 2][x] == '#':
            neighbors.append((x, y - 2))
        if y < height - 2 and maze[y + 2][x] == '#':
            neighbors.append((x, y + 2))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[(y + ny) // 2][(x + nx) // 2] = ' '
            maze[ny][nx] = ' '
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

# Exemplo de uso
maze = generate_maze(21, 21)
for row in maze:
    print(''.join(row))


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Return reversed path

        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            if 0 <= neighbor[0] < len(maze[0]) and 0 <= neighbor[1] < len(maze):
                if maze[neighbor[1]][neighbor[0]] == ' ':
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        if neighbor not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Return empty path if no path is found


def draw_maze(maze, path=None):
    cell_size = 20
    rows, cols = len(maze), len(maze[0])
    root = tk.Tk()
    canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
    canvas.pack()

    for y in range(rows):
        for x in range(cols):
            color = 'black' if maze[y][x] == '#' else 'white'
            canvas.create_rectangle(x * cell_size, y * cell_size,
                                    (x + 1) * cell_size, (y + 1) * cell_size,
                                    fill=color)

    if path:
        for (x, y) in path:
            canvas.create_rectangle(x * cell_size, y * cell_size,
                                    (x + 1) * cell_size, (y + 1) * cell_size,
                                    fill='green')

    root.mainloop()

# Exemplo de uso
start = (1, 1)
goal = (19, 19)
maze = generate_maze(21, 21)
path = a_star(maze, start, goal)
draw_maze(maze, path)
