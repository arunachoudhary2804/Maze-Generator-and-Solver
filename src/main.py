import pygame
import random

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  # Color for the endpoint
TEXT_COLOR = (255, 255, 0)  # Color for text

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

def draw_maze(screen, maze, end):
    rows, cols = len(maze), len(maze[0])
    for row in range(rows):
        for col in range(cols):
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw the endpoint symbol
    end_row, end_col = end
    pygame.draw.circle(screen, BLUE, (end_col * CELL_SIZE + CELL_SIZE // 2, end_row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

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

def draw_player(screen, player_pos):
    pygame.draw.rect(screen, GREEN, pygame.Rect(player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def display_message(screen, message):
    font = pygame.font.SysFont(None, 55)
    text_surface = font.render(message, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Maze Generator and Solver')

    def new_maze():
        rows, cols = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        maze = generate_maze(rows, cols)
        start = (1, 1)
        
        # Ensure endpoint is on the maze border and accessible
        end = (rows - 2, cols - 2)
        path = solve_maze(maze, start, end)
        return maze, start, end, path

    def reset_game():
        nonlocal maze, player_pos, end, path, game_over
        maze, player_pos, end, path = new_maze()
        game_over = False

    maze, player_pos, end, path = new_maze()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    # Regenerate the maze and reset player position
                    reset_game()
                elif event.key == pygame.K_r and game_over:
                    # Restart the game
                    reset_game()
                elif event.key == pygame.K_q and game_over:
                    # Quit the game
                    pygame.quit()
                    return
                elif event.key == pygame.K_UP and not game_over:
                    new_pos = (player_pos[0] - 1, player_pos[1])
                    if 0 <= new_pos[0] < len(maze) and maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos
                elif event.key == pygame.K_DOWN and not game_over:
                    new_pos = (player_pos[0] + 1, player_pos[1])
                    if 0 <= new_pos[0] < len(maze) and maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos
                elif event.key == pygame.K_LEFT and not game_over:
                    new_pos = (player_pos[0], player_pos[1] - 1)
                    if 0 <= new_pos[1] < len(maze[0]) and maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos
                elif event.key == pygame.K_RIGHT and not game_over:
                    new_pos = (player_pos[0], player_pos[1] + 1)
                    if 0 <= new_pos[1] < len(maze[0]) and maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos

        if player_pos == end:
            game_over = True

        screen.fill(BLACK)
        draw_maze(screen, maze, end)
        draw_solution(screen, path)
        draw_player(screen, player_pos)

        if game_over:
            display_message(screen, "Congratulations! You solved the maze. Press R to play again or Q to quit.")
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
