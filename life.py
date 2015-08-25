"""
Conway's Game of Life, as example for Matrix usage. Board starts with a random
configuration of live and dead cells and evolves automatically based on simple
rules on the number of neighbors.

Uses True for alive cells and False for dead cells.
"""
from matrix import Matrix
from random import random

class Life(object):
    def __init__(self, size=20, probability_alive=0.8):
        """ Creates a new board with given size and random live cells. """
        # The Matrix method `map` calls fn(cell_value) for every cell and builds
        # a new matrix with the results.
        self.board = Matrix(size, size).map(lambda i: random() > probability_alive)
        self.generation = 0

    def step_cell(self, pos, current):
        """
        Returns the new state of a given cell. Rules from wikipedia:

        - Any live cell with fewer than two live neighbors dies, as if caused
        by under-population.
        - Any live cell with two or three live neighbors lives on to the next
        generation.
        - Any live cell with more than three live neighbors dies, as if by
        overcrowding.
        - Any dead cell with exactly three live neighbors becomes a live cell,
        as if by reproduction.
        """        
        # Sum converts True/False to 1/0, so summing neighbors gives us the
        # number of neighbors alive.
        neighbors = sum(self.board.neighbors(*pos))
        return current if neighbors == 2 else 2 <= neighbors <= 3

    def step(self):
        """ Updates every cell and increments generation counter. """
        # The method indexmap calls fn(pos, cell_value) and builds a new matrix
        # with the results.
        self.board = self.board.indexmap(self.step_cell)
        self.generation += 1

    def show(self):
        """ Prints current generation and board. """
        print('Generation {}\n'.format(self.generation))
        print(self.board.map(lambda i: 'x' if i else '.'))

# Run without interaction.
import time
life = Life()
while True:
    life.show()
    time.sleep(0.2)
    life.step()
