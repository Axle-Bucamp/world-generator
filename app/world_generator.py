import random
from typing import List, Tuple

class World:
    def __init__(self, size: int):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.tile_types = ['grass', 'water', 'mountain', 'forest']
        self.rules = {
            'grass': ['grass', 'forest', 'mountain'],
            'water': ['water', 'grass'],
            'mountain': ['mountain', 'grass'],
            'forest': ['forest', 'grass']
        }

    def generate_world(self) -> None:
        # Start with a random tile
        start_x, start_y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        self.grid[start_y][start_x] = random.choice(self.tile_types)

        # Keep track of cells to process
        to_process = [(start_x, start_y)]

        while to_process:
            x, y = to_process.pop(0)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[ny][nx] is None:
                    possible_tiles = self.get_possible_tiles(nx, ny)
                    if possible_tiles:
                        self.grid[ny][nx] = random.choice(possible_tiles)
                        to_process.append((nx, ny))

        # Fill any remaining None cells with random tiles
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] is None:
                    self.grid[y][x] = random.choice(self.tile_types)

    def get_possible_tiles(self, x: int, y: int) -> List[str]:
        possible_tiles = set(self.tile_types)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[ny][nx] is not None:
                possible_tiles &= set(self.rules[self.grid[ny][nx]])
        return list(possible_tiles)

    def get_world_grid(self) -> List[List[str]]:
        return self.grid

def generate_world(size: int) -> List[List[str]]:
    world = World(size)
    world.generate_world()
    return world.get_world_grid()

if __name__ == "__main__":
    # Test the world generation
    size = 10
    world_grid = generate_world(size)
    for row in world_grid:
        print(" ".join(tile[:1] for tile in row))  # Print first letter of each tile type