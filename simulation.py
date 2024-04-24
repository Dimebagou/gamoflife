from grid import Grid


class Simulation:
    def __init__(self, width, height, cell_size):
        self.grid = Grid(width, height, cell_size)
        self.temp_grid = Grid(width, height, cell_size)
        self.rows = height // cell_size
        self.columns = width // cell_size
        self.run = False
        self.initial_state = None

    def draw(self, window):
        self.grid.draw(window)

    def count_live_neighbors(self, row, column):
        live_neighbors = 0

        neighbors_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1),
        ]

        for offset in neighbors_offsets:
            new_row = (row + offset[0]) % self.rows
            new_column = (column + offset[1]) % self.columns
            if self.grid.cells[new_row][new_column] == 1:
                live_neighbors += 1

        return live_neighbors

    def update(self):
        if self.is_running():
            # Création d'une nouvelle grille temporaire pour stocker les nouveaux états
            new_cells = [[0 for _ in range(self.columns)]
                         for _ in range(self.rows)]

            for row in range(self.rows):
                for column in range(self.columns):
                    live_neighbors = self.count_live_neighbors(row, column)
                    cell_value = self.grid.cells[row][column]

                    if cell_value == 1:
                        new_cells[row][column] = 1 if 2 <= live_neighbors <= 3 else 0
                    else:
                        new_cells[row][column] = 1 if live_neighbors == 3 else 0

            # Mise à jour de la grille principale avec les nouveaux états
            self.grid.cells = new_cells

    def is_running(self):
        return self.run

    def start(self):
        if not self.run:
            self.run = True
            self.initial_state = [row[:] for row in self.grid.cells]

    def stop(self):
        self.run = False

    def clear(self):
        if self.is_running() == False:
            self.grid.clear()

    def create_random_state(self):
        if self.is_running() == False:
            self.grid.fill_random()
