import random
import timeit

# Fill in the board here. (0 = value to find)

sudoku_board = [  # World's hardest sudoku (takes time on repl! PLEASE RUN LOCALLY)
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0],
]

# 8  1  2  |  7  5  3  |  6  4  9 SOLUTION
# 9  4  3  |  6  8  2  |  1  7  5
# 6  7  5  |  4  9  1  |  2  8  3
# -------------------------------
# 1  5  4  |  2  3  7  |  8  9  6
# 3  6  9  |  8  4  5  |  7  2  1
# 2  8  7  |  1  6  9  |  5  3  4
# -------------------------------
# 5  2  1  |  9  7  4  |  3  6  8
# 4  3  8  |  5  2  6  |  9  1  7
# 7  9  6  |  3  1  8  |  4  5  2

SIDE_LEN = 9  # Length and width of board
board_size = SIDE_LEN * SIDE_LEN

def get_row(board, row_num):
    return board[row_num][0:SIDE_LEN]

def get_col(board, col_num):
    return [board[i][col_num] for i in range(SIDE_LEN)]

def get_block(board, block_num):
    row = (block_num // 3) * 3
    col = (block_num * 3) % SIDE_LEN
    return [board[row + i // 3][col + i % 3] for i in range(SIDE_LEN)]

def print_board(board):
    # Used for those EPIC terminal graphics
    print("\033[2;0H", end="")
    for row in range(SIDE_LEN):
        if row in (3, 6):
            print("-------------------------------")

        for col in range(SIDE_LEN):
            if col in (3, 6):
                print("|  ", end="")
            print(board[row][col], " ", end="")
        print()

def row_col_to_block(row, col):
    return col // 3 + 3 * (row // 3)

def is_possible(board, row_num, col_num, input_num):
    row = get_row(board, row_num)
    if input_num in row:
        return False

    col = get_col(board, col_num)
    if input_num in col:
        return False

    block = get_block(board, row_col_to_block(row_num, col_num))
    if input_num in block:
        return False

    return True

def is_solved(board):

    # check if valid
    complete = set(range(1, 10))

    for i in range(SIDE_LEN):
        row = get_row(board, i)
        col = get_col(board, i)
        block = get_block(board, i)

        if set(row) != complete:
            return False
        if set(col) != complete:
            return False
        if set(block) != complete:
            return False

    return True

def next_loc(board):
    for row in range(SIDE_LEN):
        for col in range(SIDE_LEN):
            if board[row][col] == 0:
                return row, col
    return None, None

def solve(board, turn_num=-1):
    print("\033[2;0H", end="")
    print_board(board)
    count = 0
    for row in range(SIDE_LEN):
        for col in range(SIDE_LEN):
            if board[row][col] == 0:
                count += 1
    print()
    print(
        f"Turn Number: {turn_num} -- Percent Solved {100 * (board_size - count) / board_size:3.1f}%"
    )

    if is_solved(board):
        print_board(board)
        return True

    # recurse
    row, col = next_loc(board)

    if row is None:
        return False

    for val in range(1, 10):
        if is_possible(board, row, col, val):
            board[row][col] = val
            if solve(board, turn_num + 1):
                # the board is solved.
                return True
            # undo move, couldn't solve
            else:
                board[row][col] = 0

    return False

# ========================= MAIN =========================
if __name__ == "__main__":
    start = timeit.default_timer()
    try:
        if solve(sudoku_board):
            end = timeit.default_timer()
            print(f"\n\nSolution Found! -- Elapsed Time (sec): {round(end - start, 4)}")
        else:
            print("\n\nIMPOSSIBLE.")

    except KeyboardInterrupt:
        print_board(sudoku_board)
        print("\nSolving Canceled...")

