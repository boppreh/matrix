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
        m1 = Matrix()

        self.assertEqual(1, m1[0,0])
        self.assertEqual(2, m1[0,1])
        self.assertEqual(4, m1[1,0])
        self.assertEqual(9, m1[2,2])

        self.assertEqual([1, 2, 3], m1[0])
        self.assertEqual([7, 8, 9], m1[2])

if __name__ == '__main__':
    unittest.main()
