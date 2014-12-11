class Matrix(object):
    def __init__(self, height=None, width=None):
        if height is None:
            self.height = 3
            self.width = 3
            self.m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        elif width is None:
            matrix = height
            self.height = len(matrix)
            self.width = len(matrix[0])
            self.m = matrix
        else:
            self.height = height
            self.width = width
            self.m = [[None] * width for row in range(height)]

    def row(self, n):
        return list(self.m[n])

    def col(self, n):
        return [row[n] for row in self]

    def _expand_slice(self, index):
        start = list(index.start or (0, 0))
        stop = list(index.stop or (self.height, self.width))

        if start[0] < 0: start[0] += self.height
        if start[1] < 0: start[1] += self.width
        if stop[0] < 0: stop[0] += self.height
        if stop[1] < 0: stop[1] += self.width

        return slice(start, stop, index.step)

    def __iter__(self):
        for row in range(self.height):
            yield self[row]

    def __getitem__(self, index):
        if isinstance(index, tuple):
            if len(index) == 2:
                row, col = index
                return self.m[row][col]
            elif len(index) == 3:
                raise TypeError("You probably typed m[0,0:2,2] instead of m[(0,0):(2,2)].")
        elif isinstance(index, int):
            return self.m[index]
        elif isinstance(index, slice):
            index = self._expand_slice(index)

            height = index.stop[0] - index.start[0]
            width = index.stop[1] - index.start[1]

            result = Matrix(height, width)
            for row in range(height):
                for col in range(width):
                    result[row,col] = self.m[index.start[0] + row][index.start[1] + col]
            return result
        else:
            raise TypeError("Invalid index type " + str(index))

    def __setitem__(self, index, values):
        if isinstance(index, tuple):
            if len(index) == 2:
                row, col = index
                self.m[row][col] = values
            elif len(index) == 3:
                raise TypeError("You probably typed m[0,0:2,2] instead of m[(0,0):(2,2)].")
        elif isinstance(index, int):
            for i, v in enumerate(values):
                self[index,i] = v
        elif isinstance(index, slice):
            start = index.start or (0, 0)
            stop = index.stop or (self.height, self.width)

            height = stop[0] - start[0]
            width = stop[1] - start[1]

            for row in range(height):
                for col in range(width):
                    self.m[start[0] + row][start[1] + col] = values[row][col]
        else:
            raise TypeError("Invalid index type " + str(index))

    def __repr__(self):
        return '\n' + '\n'.join(' '.join(map(str, line)) for line in self.m) + '\n'

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return self.m == other.m
        else:
            return self.m == other
