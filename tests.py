import unittest
from matrix import *

class Test(unittest.TestCase):
    def test_create(self):
        m1 = Matrix(2, 3)
        m2 = Matrix([[None, None, None], [None, None, None]])
        self.assertEqual(m1, m2)
        self.assertEqual(3, m1.width)
        self.assertEqual(2, m1.height)
        self.assertEqual([[1, 2, 3], [4, 5, 6], [7, 8, 9]], Matrix())

    def test_index(self):
        m = Matrix()

        self.assertEqual(1, m[0,0])
        self.assertEqual(2, m[0,1])
        self.assertEqual(4, m[1,0])
        self.assertEqual(9, m[2,2])

        self.assertEqual([1, 2, 3], m[0])
        self.assertEqual([7, 8, 9], m[2])

    def test_slice(self):
        m = Matrix()
        self.assertEqual(m, m[(0,0):(3,3)])
        self.assertEqual(m, m[:])

        self.assertEqual([], m[(0,0):(0,0)])
        self.assertEqual([[1]], m[(0,0):(1,1)])
        self.assertEqual([[1]], m[:(1,1)])

        self.assertEqual([[1, 2], [4, 5]], m[(0,0):(2,2)])
        self.assertEqual([[5, 6], [8, 9]], m[(1,1):(3,3)])
        self.assertEqual([[5, 6], [8, 9]], m[(1,1):])
        self.assertEqual([[5, 6], [8, 9]], m[(-2,-2):])

    def test_assignment(self):
        m = Matrix()
        m[0,0] = 0
        self.assertEqual(0, m[0,0])
        m[0] = [3, 2, 1]
        self.assertEqual([3, 2, 1], m[0])
        m[(0,0):(1,1)] = [[0]]
        self.assertEqual([[0]], m[(0,0):(1,1)])
        m[(0,0):] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(Matrix(), m)

    def test_helpers(self):
        m = Matrix()

        self.assertEqual([1, 2, 3], m.row(0))
        self.assertEqual([4, 5, 6], m.row(1))
        self.assertEqual([1, 4, 7], m.col(0))
        self.assertEqual([2, 5, 8], m.col(1))
        self.assertEqual([3, 6, 9], m.col(-1))

        self.assertEqual(list(range(1, 10)), list(m.list()))

        m.addrow(1, [-1, -2, -3])
        self.assertEqual([[1, 2, 3], [-1, -2, -3], [4, 5, 6], [7, 8, 9]], m)
        m.addcol(1, [-1, -2, -3, -4])
        self.assertEqual([[1, -1, 2, 3], [-1, -2, -2, -3], [4, -3, 5, 6], [7, -4, 8, 9]], m)


if __name__ == '__main__':
    unittest.main()
