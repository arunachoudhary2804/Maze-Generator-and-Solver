import random

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

if __name__ == "__main__":
    rows, cols = 21, 21
    maze = generate_maze(rows, cols)
    for row in maze:
        print("".join(['#' if cell else ' ' for cell in row]))
