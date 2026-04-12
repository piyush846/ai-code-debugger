def is_safe(board, row, col, n):
    # Check if there is a queen in the same column
    for i in range(row):
        if board[i][col] == 1:
            return False

    # Check upper-left diagonal
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Check lower-left diagonal
    i, j = row + 1, col - 1
    while i < n and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1

    # Check upper-right diagonal
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1

    # Check lower-right diagonal
    i, j = row + 1, col + 1
    while i < n and j < n:
        if board[i][j] == 1:
            return False
        i += 1
        j += 1

    return True

def solve(board, col, n):
    if col == n:
        return True
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            if solve(board, col + 1, n):
                return True
            board[i][col] = 0

    return False

def print_board(board, n):
    for i in range(n):
        print(" ".join(str(board[i][j]) for j in range(n)))

n = 4
board = [[0] * n for _ in range(n)]
if solve(board, 0, n):
    print_board(board, n)
else:
    print("No solution")