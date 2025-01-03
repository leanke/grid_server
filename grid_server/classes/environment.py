import os
from grid_server.classes.array import GameArray
from grid_server.classes.data import object_ids, objects, item_ids

class GridWorld:
    def __init__(self, world_path):
        """
        Initialize the grid world with the given world path.
        """
        self.state_path = f"{world_path}/game_state.npy"
        if os.path.exists(self.state_path):
            self.grid = GameArray(self.state_path)
        else:
            self.grid = GameArray()
        self.time = 0
        self.return_data = None
        self.object_ids = object_ids
        self.ids_object = {value: key for key, value in object_ids.items()}

    def step(self, player, action):
        """
        Perform a game step.
        """
        self.time += 1
        if self.time % 500 == 0:
            self.grid.load_world()
        data_pack = {'text': None, 'screen': None}

        if action is not None:
            data, x, y = self.action(action, player)
            local_view = self.grid.client_view(x, y)
            data_pack['screen'] = local_view
            data_pack['text'] = data
        self.grid.save_to_file(self.state_path)
        return data_pack
    
    def interact(self, player):
        """
        Handle player interaction with the environment.
        """
        cx, cy = player.x, player.y
        direction = player.direction

        if direction == 'up':
            cx -= 1
        elif direction == 'down':
            cx += 1
        elif direction == 'left':
            cy -= 1
        elif direction == 'right':
            cy += 1
        
        if self.grid.world[cx][cy]['id'] != 0:
            ob = self.object_ids[self.grid.world[cx][cy]['id']]
            if ob == 'player':
                self.grid.remove(cx, cy)
                player.add_item(item_ids[7])
                data = f"You killed {ob}."
            elif ob == 'tree':
                data = self.handle_tree_interaction(player, cx, cy)
            else:
                data = f"Interacted with a {ob}"
        else:
            data = "Nothing to do here."
        return data

    def handle_tree_interaction(self, player, cx, cy):
        """
        Handle interaction with a tree.
        """
        data = None
        for i in player.inventory:
            if i['id'] == 7:
                self.grid.remove(cx, cy)
                player.inventory.append(item_ids[3])
                data = f"Chopped down tree"
        return data

    def action(self, action, player):
        """
        Perform an action based on the player's input.
        """
        data = None
        move = ['up', 'down', 'left', 'right']
        if action in move:
            data, x, y = self.move(action, player)
        elif action == 'interact':
            data = self.interact(player)
            x, y = player.x, player.y
        elif action == 'inventory':
            data = self.show_inventory(player)
            x, y = player.x, player.y
        elif action == 'print':
            data = player.info()
            x, y = player.x, player.y
        return data, x, y

    def show_inventory(self, player):
        """
        Show the player's inventory.
        """
        inv_list = [f"{item['name']}, " for item in player.inventory]
        return str(inv_list)
  
    def direction(self, action, player):
        """
        Determine the new coordinates based on the action.
        """
        player.direction = action
        if action == 'up':
            x = player.x - 1
            y = player.y 
        elif action == 'down':
            x = player.x + 1
            y = player.y 
        elif action == 'left':
            x = player.x
            y = player.y - 1
        elif action == 'right':
            x = player.x
            y = player.y + 1
        else:
            x = player.x
            y = player.y
        return x, y
    
    def move(self, action, player):
        """
        Move the player in the specified direction.
        """
        x, y = self.direction(action, player)
        data = None
        self.grid.move(x, y, player)
        return data, x, y
    
    def tile_info(self, player):
        """
        Get information about the tile at the specified coordinates.
        """
        cx, cy = player.x, player.y
        direction = player.direction

        if direction == 'up':
            cx -= 1
        elif direction == 'down':
            cx += 1
        elif direction == 'left':
            cy -= 1
        elif direction == 'right':
            cy += 1
        info = self.grid.world[cx][cy]
        return info
    
    def close(self):
        """
        Save the game state and close the world.
        """
        self.grid.save_to_file(self.state_path)
        print("Game saved and closed.")

