from matrix import Matrix
from itertools import groupby

size = int(input('Board size (default 3): ') or 3)
win_size = int(input('Sequence size to win (default 3): ') or 3)

# Create NxN matrix filled with numbers from 1 to N^2+1.
count = iter(range(1, size * size + 1))
board = Matrix(size, size).map(lambda i: next(count))

turn = 'x'

def check_winner():
    for line in board.rows + board.cols + board.diagonals:
        # ['x', 'x', 'o'] -> [('x', 2), ('o', 1)]
        for stone, sequence in groupby(line):
            if len(list(sequence)) == win_size:
                return stone

while True:
    print('\n{} turn:\n{}'.format(turn, board))

    while True:
        try:
            play = int(input(turn + ': '))
            assert board[play - 1] not in ('x', 'o')
            board[play - 1] = turn
            break
        except Exception:
            pass

    if check_winner():
        clean_board = board.map(lambda i: i if i in ('x', 'o') else ' ')
        print('\n{} wins!\n{}'.format(turn, clean_board))
        break
    elif all(i in ('x', 'o') for i in board):
        print('\nDraw!\n{}'.format(board))
        break

    turn = {'x': 'o', 'o': 'x'}[turn]
