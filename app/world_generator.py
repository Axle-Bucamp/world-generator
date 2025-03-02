{}

class WorldGenerator:
    def __init__(self, width, height): 
        self.width = width
        self.height = height
        # Define tile types
        self.tile_types = [Tile("grass"), Tile("dirt")]

    def init_world(self):
        return self.init_world(width, height)

    def generate_world(self):
        # Use wave function collapse algorithm to generate the world
        for x in range(self.width):
            for y in range(self.height):
                # Calculate the tile type based on the surrounding tiles
                tile_type = self.get_tile_type(x, y)
                world[x][y] = tile_type
