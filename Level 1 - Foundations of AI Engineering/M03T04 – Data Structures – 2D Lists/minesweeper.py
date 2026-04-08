def minesweeper(board):
    rows = len(board)
    cols = len(board[0])

    # Create a new board to store the counts
    result = [[0 for _ in range(cols)] for _ in range(rows)]

    # Define the directions to check for adjacent cells
    directions = [(-1, -1), (-1, 0), (-1, 1),   # NE, N, NW
                  (0, -1),           (0, 1),    # W, E
                  (1, -1), (1, 0), (1, 1)]      # SE, S, SW

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == '#':
                result[i][j] = '#'
            else:
                count = 0
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    if 0 <= x < rows and 0 <= y < cols and board[x][y] == '#':
                        count += 1
                result[i][j] = count

    return result


# Example usage:
input_board = [['-', '-', '-', '#', '#'],
               ['-', '#', '-', '-', '-'],
               ['-', '-', '#', '-', '-'],
               ['-', '#', '#', '-', '-'],
               ['-', '-', '-', '-', '-']]

output_board = minesweeper(input_board)
for row in output_board:
    print(row)
