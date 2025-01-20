import random
import numpy as np
import pickle
import base64
from grid_server.classes.data import objects_debug, walls
from grid_server.classes.tile import Tile
from grid_server.classes.noise_generator import NoiseGenerator

class GameArray:
    def __init__(self, game_state=None):
        self.object_list = objects_debug
        if game_state is not None:
            self.world = self.load_from_file(game_state)
        else:
            self.world = np.full((100, 100), Tile(), dtype=object)
            self.load_world()
        self.shape = self.world.shape

    def load_world(self) -> None:
        noise_gen = NoiseGenerator(self.world.shape)
        noise_array = noise_gen.generate_noise()

        for row in range(self.world.shape[0]):
            for cell in range(self.world.shape[1]):
                self.world[row][cell] = Tile()
        for i in range(self.world.shape[0]):
            self.world[0, i].set('object', self.get_random_wall())
            self.world[-1, i].set('object', self.get_random_wall())
            self.world[i, 0].set('object', self.get_random_wall())
            self.world[i, -1].set('object', self.get_random_wall())
        for obj in self.object_list:
            tile = self.get_tile(obj['coords'][0], obj['coords'][1])
            tile.set('object', obj['data'])
        self.world = noise_gen.generate_tiles(self.world, noise_array)


    def get_tile(self, x, y) -> Tile:
        return self.world[x][y]

    def client_view(self, entity) -> str:
        view_size = 28
        start_x = entity.x - view_size // 2
        start_y = entity.y - view_size // 2
        end_x = start_x + view_size
        end_y = start_y + view_size

        view_data = np.full((view_size, view_size), Tile(), dtype=object)

        for i in range(max(0, start_x), min(self.world.shape[0], end_x)):
            for j in range(max(0, start_y), min(self.world.shape[1], end_y)):
                view_data[i - start_x, j - start_y] = self.world[i, j]

        # Serialize the view_data array using pickle and encode it to a base64 string
        serialized_view = base64.b64encode(pickle.dumps(view_data)).decode('utf-8')
        return serialized_view, view_data

    def save_to_file(self, filename) -> None:
        with open(filename, 'wb') as file:
            np.save(file, self.world, allow_pickle=True)

    def load_from_file(self, filename) -> np.ndarray:
        with open(filename, 'rb') as f:
            world = np.load(f, allow_pickle=True)
        return world

    def remove(self, x, y, component_type) -> None:
        if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
            tile = self.get_tile(x, y)
            tile.remove(component_type)
        else:
            raise ValueError("Coordinates out of bounds")
        
    def get_random_wall(self):
        return walls[random.randint(1, 8)]
