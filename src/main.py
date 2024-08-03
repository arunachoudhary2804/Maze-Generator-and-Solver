import pygame
import random

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = []

    def visit(cell):
        row, col = cell
        maze[row][col] = 0
        stack.append(cell)

    def next_cell(cell):
        row, col = cell
        neighbors = []
        if row > 1 and maze[row - 2][col] == 1:
            neighbors.append((row - 2, col))
        if row < rows - 2 and maze[row + 2][col] == 1:
            neighbors.append((row + 2, col))
        if col > 1 and maze[row][col - 2] == 1:
            neighbors.append((row, col - 2))
        if col < cols - 2 and maze[row][col + 2] == 1:
            neighbors.append((row, col + 2))
        return random.choice(neighbors) if neighbors else None

    visit((1, 1))
    while stack:
        current = stack[-1]
        neighbor = next_cell(current)
        if neighbor:
            row, col = current
            n_row, n_col = neighbor
            maze[(row + n_row) // 2][(col + n_col) // 2] = 0
            visit(neighbor)
        else:
            stack.pop()

    return maze

def draw_maze(screen, maze):
    rows, cols = len(maze), len(maze[0])
    for row in range(rows):
        for col in range(cols):
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def solve_maze(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    path = []

    while stack:
        current = stack.pop()
        path.append(current)
        if current == end:
            return path

        row, col = current
        for d_row, d_col in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            n_row, n_col = row + d_row, col + d_col
            if 0 <= n_row < rows and 0 <= n_col < cols and maze[n_row][n_col] == 0 and (n_row, n_col) not in path:
                stack.append((n_row, n_col))

    return path

def draw_solution(screen, path):
    for cell in path:
        row, col = cell
        pygame.draw.rect(screen, RED, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Maze Generator and Solver')

    rows, cols = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
    maze = generate_maze(rows, cols)

    start = (1, 1)
    end = (rows - 2, cols - 2)
    path = solve_maze(maze, start, end)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw_maze(screen, maze)
        draw_solution(screen, path)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
