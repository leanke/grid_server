import numpy as np
from grid_server.classes.data import objects, object_ids

class GameArray:
    def __init__(self, game_state=None):
        if game_state is not None:
            self.world = self.load_from_file(game_state)
        else:
            self.world = np.zeros((100, 100), dtype=object)
            self.load_world()
        self.shape = self.world.shape
        self.ids_object = object_ids
        self.object_list = objects
        self.object_ids = {value: key for key, value in object_ids.items()}

    def load_world(self) -> None:
        for row in range(self.world.shape[0]):
            for cell in range(self.world.shape[1]):
                self.world[row][cell] = {'id': 0, 'attributes': {'type': None}}
        wall = {'id': 4, 'attributes': {'type': 'wall', 'mod': None}}
        self.world[0, :] = wall
        self.world[-1, :] = wall
        self.world[:, 0] = wall
        self.world[:, -1] = wall
        for obj in objects:
            id = obj['obj_id']
            self.place_object(obj['coords'][0], obj['coords'][1], id, obj['attr'])

    def check_object(self, x, y) -> int:
        return self.world[x][y]['id']

    def place_object(self, x, y, object_id, attributes) -> None:
        self.world[x][y] = {'id': object_id, 'attributes': attributes}
    
    def client_view(self, x, y) -> np.ndarray:
        view_size = 28
        start_x = x - view_size // 2
        start_y = y - view_size // 2
        end_x = start_x + view_size
        end_y = start_y + view_size
        start_x = max(0, start_x)
        start_y = max(0, start_y)
        end_x = min(self.world.shape[0], end_x)
        end_y = min(self.world.shape[1], end_y)
        view_data = self.world[start_x:end_x, start_y:end_y]
        
        return view_data
    
    def save_to_file(self, filename) -> None:
        with open(filename, 'wb') as file:
            np.save(file, self.world, allow_pickle=True)

    def load_from_file(self, filename) -> np.ndarray:
        with open(filename, 'rb') as f:
            world = np.load(f, allow_pickle=True)
        return world
    
    def move(self, x, y, player) -> None:
        if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
            if self.world[x][y]['id'] == 0:
                self.remove(player.x, player.y)
                player.x = x
                player.y = y
                attr = player.player_data()
                self.world[x][y] = {'id': 3, 'attributes': attr} # player.pid
        else:
            raise ValueError("Coordinates out of bounds")
    
    def remove(self, x, y):
        if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
            self.world[x][y] = {'id': 0, 'attributes': {'type': None}}
        else:
            raise ValueError("Coordinates out of bounds")
        