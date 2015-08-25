from matrix import Matrix
from random import random

class Life(object):
    def __init__(self, size=20, probability_alive=0.8):
        self.board = Matrix(size, size, 0).map(lambda i: random() > probability_alive)
        self.generation = 0

    def step_cell(self, pos, current):
        neighbors = sum(self.board.neighbors(*pos))
        return current if neighbors == 2 else 2 <= neighbors <= 3

    def step(self):
        self.board = self.board.indexmap(self.step_cell)
        self.generation += 1

    def show(self):
        print('Generation {}\n'.format(self.generation))
        print(self.board.translate(['.', 'x']))

import time
life = Life()
while True:
    life.step()
    life.show()
    time.sleep(0.2)
