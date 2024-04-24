import pygame
import random
from constants import CELL_COLOR_ALIVE, CELL_COLOR_DEAD


class Grid:
    def __init__(self, width, height, cell_size):
        self.rows = height // cell_size
        self.columns = width // cell_size
        self.cell_size = cell_size
        self.cells = [[0 for _ in range(self.columns)]
                      for _ in range(self.rows)]

    def draw(self, window):
        for row in range(self.rows):
            for column in range(self.columns):
                color = CELL_COLOR_ALIVE if self.cells[row][column] else CELL_COLOR_DEAD
                pygame.draw.rect(window, color, (column * self.cell_size, row *
                                 self.cell_size, self.cell_size - 2, self.cell_size - 2))

    def fill_random(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column] = random.choice([1, 0, 0, 0])

    def clear(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column] = 0
