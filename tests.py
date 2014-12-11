import unittest
from matrix import *

class Test(unittest.TestCase):
    def test_create(self):
        m1 = Matrix(2, 3)
        m2 = Matrix([[None, None, None], [None, None, None]])
        self.assertEqual(m1, m2)

if __name__ == '__main__':
    unittest.main()
