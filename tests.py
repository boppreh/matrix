import unittest
from matrix import *

class Test(unittest.TestCase):
    def m(self):
        return Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_create(self):
        m1 = Matrix(2, 3)
        m2 = Matrix([[None, None, None], [None, None, None]])
        self.assertEqual(m1, m2)
        self.assertEqual(3, m1.width)
        self.assertEqual(2, m1.height)
        self.assertEqual([[1, 2, 3], [4, 5, 6], [7, 8, 9]], self.m())

    def test_index(self):
        m = self.m()

        self.assertEqual(1, m[0,0])
        self.assertEqual(2, m[0,1])
        self.assertEqual(4, m[1,0])
        self.assertEqual(9, m[2,2])

        self.assertEqual([1, 2, 3], m[0])
        self.assertEqual([7, 8, 9], m[2])

    def test_slice(self):
        m = self.m()
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
        m = self.m()
        m[0,0] = 0
        self.assertEqual(0, m[0,0])
        m[0] = [3, 2, 1]
        self.assertEqual([3, 2, 1], m[0])
        m[(0,0):(1,1)] = [[0]]
        self.assertEqual([[0]], m[(0,0):(1,1)])
        m[(0,0):] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(self.m(), m)

    def test_helpers(self):
        m = self.m()

        self.assertEqual([1, 2, 3], m.row(0))
        self.assertEqual([4, 5, 6], m.row(1))
        self.assertEqual([1, 4, 7], m.col(0))
        self.assertEqual([2, 5, 8], m.col(1))
        self.assertEqual([3, 6, 9], m.col(-1))

        self.assertEqual(list(range(1, 10)), list(m.list()))
        self.assertEqual((0, 0), next(m.indices()))

        m.addrow(1, [-1, -2, -3])
        self.assertEqual([[1, 2, 3], [-1, -2, -3], [4, 5, 6], [7, 8, 9]], m)
        m.addcol(1, [-1, -2, -3, -4])
        self.assertEqual([[1, -1, 2, 3], [-1, -2, -2, -3], [4, -3, 5, 6], [7, -4, 8, 9]], m)

    def test_map(self):
        m = self.m()
        self.assertEqual([1, 4, 9], m.map(lambda v: v**2)[0])
        self.assertEqual([0, 1, 2], m.indexmap(lambda i, v: sum(i))[0])


if __name__ == '__main__':
    unittest.main()
