def minesweeper(board):
    rows = len(board)
    cols = len(board[0])

    result = [[0 for _ in range(cols)] for _ in range(rows)]

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == '#':
                result[i][j] = '#'
            else:
                count = 0
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    if (0 <= x < rows and
                            0 <= y < cols and
                            board[x][y] == '#'):
                        count += 1
                result[i][j] = count

    return result