"""
Package for a 2D pythonic Matrix data type.
"""

class Matrix(object):
    """
    2D matrix, accessible via regular indexing and slicing operators, with a
    few helper functions. All operations mutate the matrix in place, except
    `map` and `indexmap`.

    Usage:
    m = Matrix(2, 3)
    m[5] = 10
    m[(0,0):(2,2)] = m[(1,1):(2,2)]
    """
    def __init__(self, height=None, width=None, default=None):
        """
        Matrix() -> 0 by 0 matrix.
        Matrix(2, 3) -> empty matrix with 2 rows and 3 columns filled with None.
        Matrix([[1, 2], [3, 4]]) -> 2 by 2 matrix with given values.

        Matrices given are copied, not shared.
        """
        if height is None:
            self.height = 0
            self.width = 0
            self.m = []
        elif width is None:
            matrix = height
            if isinstance(matrix, Matrix):
                self.height = matrix.height
                self.width = matrix.width
            else:
                self.height = len(matrix)
                self.width = len(matrix[0])
            self.m = [[default] * self.width for row in range(self.height)]
            self[:] = matrix
        else:
            self.height = height
            self.width = width
            self.m = [[default] * width for row in range(height)]

    def __bool__(self):
        """
        A matrix is True if it has at least one item, regardless of value.
        """
        return self.height and self.width

    def index(self, value):
        """
        Returns the (row, col) of the first occurrence of `value` or None.
        """
        for row, col in self.indices():
            if self[row, col] == value:
                print(row, col)
                return value
        return None

    def row(self, n):
        """
        Returns the n'th row.
        """
        return list(self.m[n])

    def col(self, n):
        """
        Returns the n'th column.
        """
        return [row[n] for row in self.m]

    def diagonal(self, n, direction=+1):
        """
        Returns the n-th diagonal. Direction can be +1 (left to right) or -1
        (right to left). Example diagonal numbers:

        3 2 1 0
        4 3 2 1
        5 4 3 2
        """
        if n < 0 or n >= self.width + self.height - 1:
            raise IndexError('Invalid diagonal number {}.'.format(n))

        row = n - self.height
        col = 0 if direction == 1 else self.width - 1
        for i in range(self.height * 2):
            if row >= self.height or col >= self.width:
                break
            if row >= 0 and col >= 0:
                yield self[row, col]
            col += direction
            row += 1

    @property
    def rows(self):
        """ Returns a list with all rows. """
        return [self.row(i) for i in range(self.height)]

    @property
    def cols(self):
        """ Returns a list with all columns. """
        return [self.col(i) for i in range(self.width)]

    @property
    def diagonals(self):
        """
        Returns a list containing all diagonals, both left to right and right
        to left.
        """
        return ([list(self.diagonal(i, 1))
                 for i in range(self.width + self.height - 1)] +
                [list(self.diagonal(i, -1))
                 for i in range(self.width + self.height - 1)])

    def addrow(self, i, values=None):
        """
        Adds a row at the i'th position, optionally passing the list of values
        to fill the new row (defaults to all None).
        """
        self.m.insert(i, list(values or [None] * self.width))
        self.height += 1

    def addcol(self, i, values=None):
        """
        Adds a column at the i'th position, optionally passing the list of
        values to fill the new column (defaults to all None).
        """
        values = list(values or [None] * self.height)
        for row, line in enumerate(self.m):
            line.insert(i, values[row])
        self.width += 1

    def removerow(self, i):
        """ Removes the i'th row. """
        self.m.pop(i)
        self.height -= 1

    def removecol(self, i):
        """ Removes the i'th column. """
        for row in self.m:
            row.pop(i)
        self.width -= 1

    def indices(self):
        """
        Lists all indices (indexes), e.g. (0, 0), (0, 1), (0, 2), (1, 0)...
        """
        for row in range(self.height):
            for col in range(self.width):
                yield (row, col)

    def map(self, fn):
        """
        Applies `fn` to each item and stores the returned values in a new
        matrix.
    
        fn("first") -> "new_first"
        """
        result = Matrix(self.height, self.width)
        for row, col in self.indices():
            result[row, col] = fn(self[row, col])
        return result

    def indexmap(self, fn):
        """
        Applies `fn` to each index and the corresponding item, and stores
        the returned values in a new matrix.

        fn((0, 0), "first") -> "new_first"
        """
        result = Matrix(self)
        for row, col in self.indices():
            index = (row, col)
            result[index] = fn(index, self[index])
        return result

    def neighbors(self, row, col, include_diagonals=True):
        """
        Returns all values neighboring the given (row, col) position. Positions
        outside the board are omitted.

        . . . . .
        . x x x .
        . x @ x .
        . x x x .
        . . . . .

        @ x . . .
        x x . . .
        . . . . .
        . . . . .
        . . . . .

        Without `include_diagonals`:

        . . . . .
        . . x . .
        . x @ x .
        . . x . .
        . . . . .

        @ x . . .
        x . . . .
        . . . . .
        . . . . .
        . . . . .
        """
        for i in range(max(0, row - 1), min(row + 2, self.height)):
            for j in range(max(0, col - 1), min(col + 2, self.width)):
                is_diagonal = (row - i != 0) and (col - j != 0)
                if (i, j) != (row, col) and (include_diagonals or not is_diagonal):
                    yield self[i, j]

    def __len__(self):
        """
        Length  returns total number of elements, regardless of rows and
        columns.
        """
        return self.height * self.width

    def __iter__(self):
        """ Iterate through every item, in accordance to len(matrix). """
        for row, col in self.indices():
            yield self.m[row][col]

    def __in__(self, item):
        """ Searches for an item. """
        for v in self:
            if v == item:
                return True
        return False

    def _expand_slice(self, index):
        """
        Returns (start, stop) from the given slice, filling with expected
        values when not present and supporting negative indices.
        """
        start = list(index.start or (0, 0))
        stop = list(index.stop or (self.height, self.width))

        if start[0] < 0: start[0] += self.height
        if start[1] < 0: start[1] += self.width
        if stop[0] < 0: stop[0] += self.height
        if stop[1] < 0: stop[1] += self.width

        return (start[0], start[1]), (stop[0], stop[1])

    def _row_col_to_index(self, row, col):
        return row * self.width + col

    def _index_to_row_col(self, index):
        return index // self.width, index % self.width

    def getdefault(self, row, col, default):
        if row < 0 or col < 0 or row >= self.width or col >= self.height:
            return default
        return self[row, col]

    def __getitem__(self, index):
        """
        Reads values from the matrix. Index can be a int (returning the i'th
        item), a (row, col) tuple or a slice object of the those. Thus it may
        return a single value or a new matrix.
        """
        if isinstance(index, tuple):
            if len(index) == 2:
                row, col = index
                return self.m[row][col]
            elif len(index) == 3:
                raise TypeError("You probably typed m[0,0:2,2] instead of m[(0,0):(2,2)].")
        elif isinstance(index, int):
            row, col = self._index_to_row_col(index)
            return self.m[row][col]
        elif isinstance(index, slice):
            t = index.start or index.stop
            if isinstance(t, int):
                return list(self)[index]
            else:
                (row0, col0), (row1, col1) = self._expand_slice(index)

                height = row1 - row0
                width = col1 - col0

                result = Matrix(height, width)
                for row in range(height):
                    for col in range(width):
                        result[row,col] = self.m[row0 + row][col0 + col]
                return result
        else:
            raise TypeError("Invalid index type " + str(index))

    def __setitem__(self, index, values):
        """
        Writes values to the the matrix. Index can be a int (returning the i'th
        item), a (row, col) tuple or a slice object of the those. `values` must
        be a single value or a matrix depending on the type of index used.
        """
        if isinstance(index, tuple):
            if len(index) == 2:
                row, col = index
                self.m[row][col] = values
            elif len(index) == 3:
                raise TypeError("You probably typed m[0,0:2,2] instead of m[(0,0):(2,2)].")
        elif isinstance(index, int):
            row, col = self._index_to_row_col(index)
            self.m[row][col] = values
        elif isinstance(index, slice):
            t = index.start or index.stop
            if isinstance(t, int):
                start, stop, stride = index.indices(len(self))
                for i, j in enumerate(range(start, stop, stride)):
                    self[i] = values[i]
            else:
                (row0, col0), (row1, col1) = self._expand_slice(index)
                if isinstance(values, Matrix):
                    values = values.m
                for row in range(row1 - row0):
                    for col in range(col1 - col0):
                        self.m[row0 + row][col0 + col] = values[row][col]
        else:
            raise TypeError("Invalid index type " + str(index))

    def __repr__(self):
        """
        Returns a multi-line string representation of the matrix. Columns are
        aligned based on the largest item.

         1  2  3  4
         5  6  7  8
         9 10 11 12
        13 14 15 16
        """
        max_length = max(len(str(i)) for i in self)
        template = '{: >' + str(max_length) + '}'
        lines = (' '.join(map(template.format, line)) for line in self.m)
        return '\n'.join(lines) + '\n'

    def __eq__(self, other):
        """ Equality testing allows comparing to list of lists. """
        if isinstance(other, Matrix):
            return self.m == other.m
        else:
            return self.m == other or list(self) == other

class _AbstractCursor(object):
    def __init__(self, board, row=None, col=None):
        self.board = board
        self.row = row if row is not None else self.board.height // 2
        self.col = col if col is not None else self.board.width // 2
        self.symbol = '@'

    def move(self, drow, dcol):
        if drow == -1: self.up()
        if drow == 1: self.down()
        if dcol == -1: self.left()
        if dcol == 1: self.right()

    @property
    def value(self):
        return self.board[self.row, self.col]

    @value.setter
    def value(self, v):
        self.board[self.row, self.col] = v

    @property
    def movements(self):
        return {'up': self.up, 'down': self.down, 'right': self.right, 'left': self.left}

    @property
    def display(self):
        old = self.board[self.row, self.col]
        self.board[self.row, self.col] = self.symbol
        text = str(self.board)
        self.board[self.row, self.col] = old
        return text

    def __repr__(self):
        return '{}(row={}, col={}, board={}x{})'.format(self.__class__.__name__, self.row, self.col, self.board.height, self.board.width)

class WrappingCursor(_AbstractCursor):
    def up(self):
        self.row = (self.row - 1 + self.board.height) % self.board.height
    def down(self):
        self.row = (self.row + 1 + self.board.height) % self.board.height
    def right(self):
        self.col = (self.col + 1 + self.board.height) % self.board.width
    def left(self):
        self.col = (self.col - 1 + self.board.height) % self.board.width

class DefaultingCursor(_AbstractCursor):
    def __init__(self, board, default=None, row=None, col=None):
        self.default = default
        super(DefaultingCursor, self).__init__(board, row, col)

    def up(self): self.row += 1
    def down(self): self.row -= 1
    def right(self): self.col += 1
    def left(self): self.col -= 1

    @property
    def is_valid(self):
        return self.col >= 0 and self.row >= 0 and self.col < self.board.width and self.row < self.board.height

    @property
    def value(self):
        return self.board[self.row, self.col] if self.is_valid else self.default

    @value.setter
    def set_value(self, v):
        if self.is_valid:
            self.board[self.row, self.col] = v

    @property
    def display(self):
        if not self.is_valid:
            return repr(self.board)
        return _AbstractCursor.display.fget(self)

class BoundedCursor(_AbstractCursor):
    def up(self):
        if self.row > 0:
            self.row -= 1

    def down(self):
        if self.row < self.board.height - 1:
            self.row += 1

    def left(self):
        if self.col > 0:
            self.col -= 1

    def right(self):
        if self.col < self.board.width - 1:
            self.col += 1
