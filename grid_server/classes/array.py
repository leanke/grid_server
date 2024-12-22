
import numpy as np
from grid_server.classes.data import objects, test_array


class GameArray:
    def __init__(self, game=test_array):
        self.game = game
        if game is not None:
            x, y = game.shape
            self.width = x
            self.height = y
            self.object = objects
        else:
            self.width = 20
            self.height = 20
            self.object = objects
            self.game = np.zeros((self.height, self.width), dtype=np.int8)
            self.object = objects

    def build_array_from_json(self, config):
        self.game = np.zeros((config["height"], config["width"]), dtype=np.int8)
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

    def load_objects(self):
        for obj_id, objv in self.object.items():
            for obj in objv:
                self.place_object(obj['x'], obj['y'], obj_id)

    def place_object(self, x, y, obj_id):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.game[y][x] = obj_id
        else:
            raise ValueError("Coordinates out of bounds")
        
    def move(self, x, y, player):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.game[y][x] = 3
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