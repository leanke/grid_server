
import numpy as np
from grid_server.classes.data import objects, test_array
# from grid_server.classes.data import test_object_ids as object_ids
from grid_server.classes.object_list import object_list, test_list
from grid_server.classes.test_data import object_ids
from grid_server.classes.test_data import ids_object


class GameArray:
    def __init__(self, game=None):
        self.game = game
        if game is not None:
            x, y = game.shape
            self.width = x
            self.height = y
            self.object = objects
        else:
            self.width = 20
            self.height = 20
            self.game = np.zeros((self.height, self.width), dtype=np.int32)
            self.object = objects

    def build_array_from_json(self, config):
        self.game = np.zeros((config["height"], config["width"]), dtype=np.int32)
        self.object = config["object"]
        self.load_objects()
        return self.game

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            np.save(file, self.game, allow_pickle=True)

    def load_from_file(self, filename):
        with open(filename, 'rb') as f:
            self.game = np.load(f)
        return self.game
    
    def move(self, x, y, player):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.game[y][x] = 3
        else:
            raise ValueError("Coordinates out of bounds")

    def load_objects(self):
        for obj_id, objv in self.object.items():
            for obj in objv:
                self.place_object(obj['x'], obj['y'], obj_id)

    def place_object(self, x, y, obj_id):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.game[y][x] = obj_id
        else:
            raise ValueError("Coordinates out of bounds")
    
    def update(self, flag=False):
        self.load_objects()
        return self.game

    def remove(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.game[y][x] = 0
        else:
            raise ValueError("Coordinates out of bounds")

class GameArrayTest:
    def __init__(self, array_shape):
        self.shape = array_shape
        self.world = np.zeros(array_shape, dtype=int)
        self.object_ids = object_ids
        self.object_list = test_list # object_list
        self.ids_object = ids_object

    def load_world(self) -> None:
        for obj in self.object_list:
            # print(obj)
            id = self.object_ids[obj['obj_id']]
            self.place_object(obj['coords'][0], obj['coords'][1], id)

    def check_object(self, x, y) -> int:
        return self.ids_object[self.world[x][y]]

    def place_object(self, x, y, object_id) -> None:
        self.world[x][y] = object_id

    def remove_object(self, x, y) -> None:
        self.world[x][y] = 0

    def get_world(self) -> np.ndarray:
        return self.world

    def get_shape(self) -> tuple:
        return self.shape
    
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
        # print(view_data)
        return view_data
    
    
    def debug_world(self) -> None:
        print(f'{self.world}')

    def save_to_file(self, filename) -> None:
        with open(filename, 'wb') as file:
            np.save(file, self.world, allow_pickle=True)

    def load_from_file(self, filename) -> np.ndarray:
        with open(filename, 'rb') as f:
            self.world = np.load(f)
        return self.world
    
    def move(self, x, y, player) -> None:
        if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
            self.world[x][y] = 3 # player.id
        else:
            raise ValueError("Coordinates out of bounds")
    
    def remove(self, x, y):
        if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
            self.world[x][y] = 0
        else:
            raise ValueError("Coordinates out of bounds")

# class IDTable:
#     def __init__(self):
#         self.entities = {}
#         self.next_id = 1

#     def add_entity(self, entity):
#         entity_id = self.next_id
#         self.entities[entity_id] = entity
#         self.next_id += 1
#         return entity_id

#     def get_entity(self, entity_id):
#         return self.entities.get(entity_id)

#     def update_entity(self, entity_id, attr_name, attr_value):
#         entity = self.get_entity(entity_id)
#         if entity:
#             if hasattr(entity, attr_name):
#                 setattr(entity, attr_name, attr_value)
#             else:
#                 raise AttributeError(f"{attr_name} is not a valid attribute of {type(entity).__name__}")
#         else:
#             raise ValueError(f"Entity with ID {entity_id} not found")
# >>> import numpy as np
# >>> from tempfile import TemporaryFile
# >>> outfile = TemporaryFile()
# >>> x = np.arange(10)
# >>> np.save(outfile, x)
# >>> _ = outfile.seek(0) # Only needed to simulate closing & reopening file
# >>> np.load(outfile)
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# >>> with open('test.npy', 'wb') as f:
# ...     np.save(f, np.array([1, 2]))
# ...     np.save(f, np.array([1, 3]))
# >>> with open('test.npy', 'rb') as f:
# ...     a = np.load(f)
# ...     b = np.load(f)