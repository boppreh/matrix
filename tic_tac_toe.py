"""
Generalized Tic Tac Toe game for any board size, as example for Matrix usage.
"""
from matrix import Matrix
from collections import defaultdict

size = int(input('Board size (default 3): ') or 3)
win_size = int(input('Sequence size to win (default 3): ') or 3)

# The Matrix method `map` calls fn(cell_value) for every cell and builds a new
# matrix with the results. Here we fill the matrix with numbers from 1 to
# N^2+1.
count = (str(i) for i in range(1, size * size + 1))
board = Matrix(size, size, data=count, default='')

turn = 'x'

while True:
    # When converted to string, the board prints itself as a NxM matrix with
    # aligned columns, such as this:
    #
    #  1  2  3  4
    #  5  6  7  8
    #  9 10 11 12
    print('\n{} turn:\n{}'.format(turn, board))

    while True:
        try:
            play = input(turn + ': ')
            # Player entered a number, now search for this number in our board.
            row, col = board.index(play)
            assert board[row, col] not in ('x', 'o')
            board[row, col] = turn
            break
        except Exception as e:
            print(e)
            pass

    # Make a list of all lines that pass through the cell played.
    directions = [board.row(row),
                  board.col(col),
                  board.diagonal(row, col, +1),
                  board.diagonal(row, col, -1)]

    # Convert lines to a single space separated string.
    str_directions = ' '.join(''.join(line) for line in directions)

    # Verify if there are three of the player symbols in a row.
    if turn * 3 in str_directions:
        # Maps every cell removing the ones that are still numbers.
        clean_board = board.map(lambda i: i if i in 'xo' else '')
        print('\n{} wins!\n{}'.format(turn, clean_board))
        break()

    if all(i in ('x', 'o') for i in board):
        print('\nDraw!\n{}'.format(board))
        break

    turn = {'x': 'o', 'o': 'x'}[turn]
