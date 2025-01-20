import random
import numpy as np
import noise
from grid_server.classes.tile import Tile
from grid_server.classes.data import trees, rocks

class NoiseGenerator:
    def __init__(self, shape, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0):
        self.shape = shape
        self.scale = scale
        self.oct = octaves
        self.per = persistence
        self.lac = lacunarity

    def generate_noise(self):
        world = np.zeros(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                world[i][j] = noise.pnoise2(
                    i / self.scale, 
                    j / self.scale, 
                    octaves=self.oct,
                    persistence=self.per,
                    lacunarity=self.lac,
                    repeatx=self.shape[0],
                    repeaty=self.shape[1],
                    base=42)
        return world

    def generate_tiles(self, world, noise_array):
        tiles = world
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                rand = random.randint(10, 20)
                if i != 0 and i != self.shape[0] - 1 and j != 0 and j != self.shape[1] - 1 and tiles[i][j].get('object') is None:
                    if noise_array[i][j] > 0.01:
                        if not self._is_near_existing_object(tiles, i, j, rand) and random.random() > 0.5:
                            tiles[i][j].set('object', trees[random.randint(1, len(trees) - 1)])
                    else:
                        if not self._is_near_existing_object(tiles, i, j, rand) and random.random() > 0.5:
                            tiles[i][j].set('object', rocks[random.randint(1, len(rocks) - 1)])
        return tiles

    def _is_near_existing_object(self, tiles, x, y, rand):
        count = 0
        for i in range(max(0, x-rand), min(self.shape[0], x+rand+1)):
            for j in range(max(0, y-rand), min(self.shape[1], y+rand+1)):
                if tiles[i][j].get('object') is not None:
                    count += 1
        return count >= 3
