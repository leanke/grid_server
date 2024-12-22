import json
import os
from grid_server.classes.array import GameArray
from grid_server.classes.data import obj_ids, objects

class GridWorld:
    def __init__(self, config):
        self.config = config
        self.array_path = config['array_path']
        self.time = 0
        self.return_data = None
        if config['new_world'] == 'True':
            with open('grid_server/world.json', 'r') as grid_json:
                grid_config = json.load(grid_json)
                grid = GameArray().build_array_from_json(grid_config)
                print("Created new world: ", self.config['world_name'])
        else:
            grid = GameArray().load_from_file(self.array_path)
            grid[grid == 3] = 0
            print(f"loaded {self.config['world_name']} from file")
        self.grid = GameArray(grid)
        
    
    def step(self, player, action):
        data = None
        self.time += 1
        if action is not None:
            data = self.action(action, player)
            print(f"{player.name} took action {action}")
        self.grid.save_to_file(self.array_path)
        return data
        

    def action(self, action, player):
            data = None
            if action == 'up':
                x = player.x
                y = player.y - 1
            elif action == 'down':
                x = player.x
                y = player.y + 1
            elif action == 'left':
                x = player.x - 1
                y = player.y
            elif action == 'right':
                x = player.x + 1
                y = player.y
            elif action == 'print':
                x = player.x
                y = player.y
                data = player.info()
            if self.grid.game[y][x] != 3:
                if self.grid.game[y][x] != 0:
                    object_id = self.grid.game[y][x]
                    ob = obj_ids[object_id]
                    data = f"Can't move there. {ob} in the way."
                    x = player.x
                    y = player.y
                else:
                    self.grid.move(x, y, player)
                    self.grid.remove(player.x, player.y)
            player.save('stats', 'x', x)
            player.save('stats', 'y', y)
            return data

