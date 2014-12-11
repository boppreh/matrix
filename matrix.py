class Matrix(object):
    def __init__(self, nrows=None, ncols=None):
        if nrows is None:
            self.nrows = 3
            self.ncols = 3
            self.m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        elif ncols is None:
            matrix = nrows
            self.nrows = len(matrix)
            self.ncols = len(matrix[0])
            self.m = matrix
        else:
            self.nrows = nrows
            self.ncols = ncols
            self.m = [[None] * ncols for row in range(nrows)]

        self.height = nrows
        self.width = ncols

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.m[index]
        elif isinstance(index, tuple):
            row, col = index
            return self.m[row][col]
        else:
            raise TypeEror("Invalid index type " + str(index))

    def __repr__(self):
        return '\n'.join(' '.join(map(str, line)) for line in self.m)

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return self.m == other.m
        else:
            return self.m == other
