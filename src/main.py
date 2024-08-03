GREEN = (0, 255, 0)

def draw_player(screen, player_pos):
    pygame.draw.rect(screen, GREEN, pygame.Rect(player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Maze Generator and Solver')

    def new_maze():
        rows, cols = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        maze = generate_maze(rows, cols)
        start = (1, 1)
        end = (rows - 2, cols - 2)
        return maze, start, end

    maze, player_pos, end = new_maze()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    maze, player_pos, end = new_maze()
                elif event.key == pygame.K_UP:
                    new_pos = (player_pos[0] - 1, player_pos[1])
                    if maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos
                elif event.key == pygame.K_DOWN:
                    new_pos = (player_pos[0] + 1, player_pos[1])
                    if maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos
                elif event.key == pygame.K_LEFT:
                    new_pos = (player_pos[0], player_pos[1] - 1)
                    if maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = (player_pos[0], player_pos[1] + 1)
                    if maze[new_pos[0]][new_pos[1]] == 0:
                        player_pos = new_pos

        screen.fill(BLACK)
        draw_maze(screen, maze)
        draw_player(screen, player_pos)
        pygame.display.flip()

        if player_pos == end:
            print("Maze solved!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
