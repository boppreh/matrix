"""
Package for a 2D pythonic Matrix data type. Exports only the Matrix class.
"""

class Matrix(object):
    """
    2D matrix, accessible via regular indexing and slicing operators, with a
    few helper functions. All operations mutate the matrix in place, except
    `map` and `indexedmap`.

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

    def addrow(self, i, values=None):
        """
        Adds a row at the i'th position, optionally passing the list of values
        to fill the new row (defaults to all None).
        """
        self.m.insert(i, values or [None] * self.width)
        self.height += 1

    def addcol(self, i, values=None):
        """
        Adds a column at the i'th position, optionally passing the list of
        values to fill the new column (defaults to all None).
        """
        values = values or [None] * self.height
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
            row = index // self.width
            col = index % self.width
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
            row = index // self.width
            col = index % self.width
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
        1 2 3
        4 5 6
        7 8 9
        """
        return '\n' + '\n'.join(' '.join(map(str, line)) for line in self.m) + '\n'

    def __eq__(self, other):
        """ Equality testing allows comparing to list of lists. """
        if isinstance(other, Matrix):
            return self.m == other.m
        else:
            return self.m == other or list(self) == other
