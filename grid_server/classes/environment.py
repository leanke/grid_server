from grid_server.classes.array import GameArray, GameArrayTest
from grid_server.classes.data import obj_ids, objects

class GridWorld:
    def __init__(self, shape, path):
        self.grid = GameArrayTest(shape)
        
        self.path = path
        self.time = 0
        self.return_data = None

    def step(self, player, action):
        self.time += 1
        data_pack = {'text': None, 'screen': None}

        if action is not None:
            data, x, y = self.action(action, player)
            local_view = self.grid.client_view(x, y)
            data_pack['screen'] = local_view
            data_pack['text'] = data
            # print(f"{player.name} took action {action}")
            # print(f"{player.name} coords: {player.x}, {player.y}")
        ret = data_pack
        self.grid.save_to_file(f"{self.path}/game_state.npy")
        return ret
    
    def interact(self, player):
        cx, cy = player.x, player.y,
        direction = player.direction

        if direction == 'up':
            cx -= 1
        elif direction == 'down':
            cx += 1
        elif direction == 'left':
            cy -= 1
        elif direction == 'right':
            cy += 1
        
        if self.grid.world[cx][cy] != 0:
            ob = obj_ids[self.grid.world[cx][cy]]
            data = f"Interacted with a {ob}"
        else:
            data = "Nothing to do here."
        return data

    def action(self, action, player):
        data = None
        move = ['up', 'down', 'left', 'right']
        if action in move:

            data, x, y = self.move(action, player)
            return data, x, y
        elif action == 'interact':
            data = self.interact(player)
            return data, player.x, player.y
        elif action == 'inventory':
            data = str(player.inventory)
            return data, player.x, player.y
        elif action == 'print':
            data = player.info()
            return data, player.x, player.y
  
    def move(self, action, player):
        player.direction = action
        if action == 'up':
            x = player.x - 1
            y = player.y 
        elif action == 'down':
            x = player.x + 1 # 
            y = player.y 
        elif action == 'left':
            x = player.x
            y = player.y - 1 # 
        elif action == 'right':
            x = player.x
            y = player.y + 1 # 

        if self.grid.world[x][y] != 0:
            if self.grid.world[x][y] != 3:
                object_id = self.grid.world[x][y]
                ob = obj_ids[object_id]
                data = f"Can't move there. A {ob} is in the way."
                x = player.x
                y = player.y
        else:
            self.grid.move(x, y, player)
            self.grid.remove(player.x, player.y)
            player.x = x
            player.y = y
            data = None
        return data, x, y

