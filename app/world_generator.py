import random
class World:
    def __init__(self, size):
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def define_tile_types(self):
        tile_types = ['water', 'land', 'dirt']
        return tile_types

    def generate_world(self, size):
        tile_types = self.define_tile_types()
        for i in range(size):
            for j in range(size):
                if random.random() < 0.5:
                    self.grid[i][j] = tile_types[0]
                else:
                    self.grid[i][j] = tile_types[1]