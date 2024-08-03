import pygame
import random
from collections import deque

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Color for player
BLUE = (0, 0, 255)   # Color for the end point
FPS = 60

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

def find_farthest_point(maze, start):
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = set([start])
    farthest_point = start

    while queue:
        point = queue.popleft()
        farthest_point = point
        row, col = point
        for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            n_row, n_col = row + d_row, col + d_col
            if 0 <= n_row < rows and 0 <= n_col < cols and maze[n_row][n_col] == 0 and (n_row, n_col) not in visited:
                queue.append((n_row, n_col))
                visited.add((n_row, n_col))

    return farthest_point

def draw_maze(screen, maze):
    rows, cols = len(maze), len(maze[0])
    for row in range(rows):
        for col in range(cols):
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player(screen, player_pos):
    pygame.draw.rect(screen, GREEN, pygame.Rect(player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_end_point(screen, end_pos):
    pygame.draw.rect(screen, BLUE, pygame.Rect(end_pos[1] * CELL_SIZE, end_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Maze Generator and Solver')
    clock = pygame.time.Clock()

    def new_maze():
        rows, cols = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        maze = generate_maze(rows, cols)
        start = (1, 1)
        end = find_farthest_point(maze, start)
        return maze, start, end

    maze, player_pos, end = new_maze()

    running = True
    won = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    maze, player_pos, end = new_maze()
                    won = False
                elif event.key == pygame.K_SPACE:
                    maze, player_pos, end = new_maze()
                    won = False
                elif event.key == pygame.K_UP:
                    new_pos = (player_pos[0] - 1, player_pos[1])
                    if 0 <= new_pos[0] < len(maze) and maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos
                elif event.key == pygame.K_DOWN:
                    new_pos = (player_pos[0] + 1, player_pos[1])
                    if 0 <= new_pos[0] < len(maze) and maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos
                elif event.key == pygame.K_LEFT:
                    new_pos = (player_pos[0], player_pos[1] - 1)
                    if 0 <= new_pos[1] < len(maze[0]) and maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = (player_pos[0], player_pos[1] + 1)
                    if 0 <= new_pos[1] < len(maze[0]) and maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos

        # Check if player reached the end
        if player_pos == end:
            won = True

        screen.fill(BLACK)
        draw_maze(screen, maze)
        draw_player(screen, player_pos)
        draw_end_point(screen, end)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
