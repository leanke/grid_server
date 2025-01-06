import numpy as np
import pickle
import base64
from grid_server.classes.data import objects_debug, object_ids, item_ids, walls
from grid_server.classes.objects import GameObject
from grid_server.classes.tile import Tile

class GameArray:
    def __init__(self, game_state=None):
        self.ids_object = object_ids
        self.object_list = objects_debug
        self.object_ids = {value: key for key, value in object_ids.items()}
        if game_state is not None:
            self.world = self.load_from_file(game_state)
        else:
            self.world = np.full((100, 100), Tile(), dtype=object)
            self.load_world()
        self.shape = self.world.shape

    def load_world(self) -> None:
        for row in range(self.world.shape[0]):
            for cell in range(self.world.shape[1]):
                self.world[row][cell] = Tile()
        wall_tile = Tile(object=walls[1])
        self.world[0, :] = wall_tile
        self.world[-1, :] = wall_tile
        self.world[:, 0] = wall_tile
        self.world[:, -1] = wall_tile
        for obj in self.object_list:
            self.place_object(obj['coords'][0], obj['coords'][1], obj['data'])

    def check_tile(self, x, y) -> Tile:
        return self.world[x][y]

    def place_object(self, x, y, obj) -> None:
        tile = self.check_tile(x, y)
        tile.set_object(obj)

    def place_entity(self, x, y, entity) -> None:
        tile = self.check_tile(x, y)
        tile.set_entity(entity)

    def place_item(self, x, y, item) -> None:
        tile = self.check_tile(x, y)
        tile.set_item(item)

    def client_view(self, player) -> str:
        view_size = 28
        start_x = player.x - view_size // 2
        start_y = player.y - view_size // 2
        end_x = start_x + view_size
        end_y = start_y + view_size
        if view_size != 28:
            player.local_x = view_size // 2
            player.local_y = view_size // 2

        view_data = np.full((view_size, view_size), Tile(), dtype=object)

        for i in range(max(0, start_x), min(self.world.shape[0], end_x)):
            for j in range(max(0, start_y), min(self.world.shape[1], end_y)):
                view_data[i - start_x, j - start_y] = self.world[i, j]

        # Serialize the view_data array using pickle and encode it to a base64 string
        serialized_view = base64.b64encode(pickle.dumps(view_data)).decode('utf-8')
        return serialized_view

    def save_to_file(self, filename) -> None:
        with open(filename, 'wb') as file:
            np.save(file, self.world, allow_pickle=True)

    def load_from_file(self, filename) -> np.ndarray:
        with open(filename, 'rb') as f:
            world = np.load(f, allow_pickle=True)
        return world
    
    def move(self, x, y, player) -> None:
        if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
            tile = self.check_tile(x, y)
            if tile.object is None and tile.entity is None:
                self.remove(player.x, player.y)
                player.x = x
                player.y = y
                attr = player.player_data()
                self.place_entity(x, y, attr)
        else:
            raise ValueError("Coordinates out of bounds")
    
    def remove(self, x, y):
        if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
            self.world[x][y].clear()
        else:
            raise ValueError("Coordinates out of bounds")
