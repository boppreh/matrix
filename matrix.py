class Matrix(object):
    def __init__(self, nrows, ncols=None):
        if ncols is None:
            matrix = nrows
            self.m = matrix
            self.nrows = len(matrix)
            self.ncols = len(matrix[0])
        else:
            self.nrows = nrows
            self.ncols = ncols
            self.m = [[None] * ncols for row in range(nrows)]

    def __eq__(self, other):
        return isinstance(other, Matrix) and self.m == other.m
