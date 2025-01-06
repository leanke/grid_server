import os
from grid_server.classes.array import GameArray
from grid_server.classes.data import object_ids, item_ids

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
        if self.time % 1000 == 0:
            self.grid.load_world()
        # data_pack = {'text': None, 'screen': None}
        data = None
        if action is not None:
            text, x, y = self.action(action, player)
            # local_view = self.grid.client_view(x, y)
            # data_pack['screen'] = local_view
            data = text
        self.grid.save_to_file(self.state_path)
        return data
    
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
        
        target_tile = self.grid.world[cx][cy]
        interaction_result = self.handle_interaction(player, target_tile)
        return interaction_result

    def handle_interaction(self, player, target_tile):
        """
        Handle interactions with different types of tiles.
        """
        if target_tile['tile']['object']:
            return self.handle_object_interaction(player, target_tile['tile']['object'])
        elif target_tile['tile']['entity']:
            return self.handle_entity_interaction(player, target_tile['tile']['entity'])
        elif target_tile['tile']['item']:
            return self.handle_item_interaction(player, target_tile['tile']['item'])
        else:
            return "Nothing to do here."

    def handle_object_interaction(self, player, obj):
        """
        Handle interaction with an object.
        """
        if obj['type'] == 'tree':
            return self.handle_tree_interaction(player, obj)
        else:
            return f"Interacted with a {obj['name']}"

    def handle_entity_interaction(self, player, entity):
        """
        Handle interaction with an entity.
        """
        if entity['type'] == 'player':
            self.grid.remove(entity['coords']['x'], entity['coords']['y'])
            player.add_item(item_ids[7])
            return f"You killed {entity['name']}."
        else:
            return f"Interacted with a {entity['name']}"

    def handle_item_interaction(self, player, item):
        """
        Handle interaction with an item.
        """
        player.add_item(item)
        self.grid.remove(item['coords']['x'], item['coords']['y'])
        return f"Picked up {item['name']}."

    def handle_tree_interaction(self, player, tree):
        """
        Handle interaction with a tree.
        """
        for i in player.inventory:
            if i['id'] == 7:
                self.grid.remove(tree['coords']['x'], tree['coords']['y'])
                self.grid.place_item(tree['coords']['x'], tree['coords']['y'], item_ids[3])
                return "Chopped down tree"
        return "You need an axe to chop down this tree."

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

