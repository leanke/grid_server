import os
from grid_server.classes.array import GameArray
from grid_server.classes.entities.entity import Entity
from grid_server.classes.entities.player import Player

class GridWorld:
    def __init__(self, world_path):
        self.state_path = f"{world_path}/game_state.npy"
        if os.path.exists(self.state_path):
            self.grid = GameArray(self.state_path)
        else:
            self.grid = GameArray()
        self.time = 0
        self.return_data = None
        self.save_freq = 0 # save file for auto load

    def step(self, entity, action):
        self.time += 1
        # if self.time % 1000 == 0:
        #     self.grid.load_world()
        data = None
        if action is not None:
            text = self.action(action, entity)
            data = text
        if self.save_freq != 0 and self.time % self.save_freq == 0:
            self.grid.save_to_file(self.state_path)
        return data
    
    def action(self, action, entity):
        data = None
        move = ['up', 'down', 'left', 'right']
        if action in move:
            self.move(action, entity)
            data = ''
        elif action == 'interact':
            data = self.interact(entity)
        elif action == 'attack':
            data = self.attack(entity)
        else:
            data = f"Invalid action: {action}"
        return data

    def interact(self, entity):
        cx, cy = self.direction(entity.direction, entity)
        target_tile = self.grid.world[cx][cy]
        if target_tile.object:
            return self.object_interaction(entity, target_tile.object)
        elif target_tile.entity:
            if isinstance(target_tile.entity, Entity):
                return f"{entity.name} interacted with {target_tile.entity.name}."
        elif target_tile.items:
            entity.pick_up(target_tile.items[0])
            return f"Picked up a {target_tile.items[0]['name']}."
        else:
            return "Nothing to do here."
        
    def direction(self, action, entity):
        cx, cy = entity.x, entity.y
        entity.direction = action

        if action == 'up':
            cx -= 1
        elif action == 'down':
            cx += 1
        elif action == 'left':
            cy -= 1
        elif action == 'right':
            cy += 1
        return cx, cy
    
    def move(self, action, entity):
        x, y = self.direction(action, entity)
        if 0 <= x < self.grid.shape[0] and 0 <= y < self.grid.shape[1]:
            old_tile = self.grid.get_tile(entity.x, entity.y)
            new_tile = self.grid.get_tile(x, y)
            if new_tile.object is None and new_tile.entity is None:
                old_tile.remove('entity')
                entity.x = x
                entity.y = y
                attr = entity.entity_data()
                new_tile.set('entity', entity)
            else:
                return "Cannot move to that tile"
        else:
            return "Coordinates out of bounds"
    
    def close(self):
        if self.save_freq != 0:
            self.grid.save_to_file(self.state_path)

    def attack(self, entity):
        target_damage = entity.attack() # {'left':{'damage': 0, 'target': []}, 'right':{'damage': 0, 'target': []}}
        for k, v in target_damage.items():
            for target in v['target']:

                target_tile = self.grid.get_tile(target[0], target[1])
                target_entity = target_tile.entity
                if target_entity != entity and target_entity is not None: #isinstance(target_entity, Player) and 
                    target_x = target_entity.x
                    target_y = target_entity.y
                    is_dead, drops = target_entity.receive_damage(v['damage'])
                    if is_dead:
                        for drop in drops:
                            if drop != {}:
                                self.grid.get_tile(target_x, target_y).set('item', drop)
                        self.grid.get_tile(target_x, target_y).remove('entity')
                        entity.x = target_entity.home[0]
                        entity.y = target_entity.home[1]
                        self.grid.get_tile(target_entity.home[0], target_entity.home[1]).set('entity', target_entity)
                        return f"{target_entity.name} has died."
                    return f"Engaged in combat with {target_entity.name}."
                else:
                    return "no entity to attack"

    def object_interaction(self, entity, obj):
        # print(obj)
        if obj['id'] == 1:
            return self.tree_interaction(entity, obj)
        elif obj['id'] == 2:
            return self.rock_interaction(entity, obj)
        # elif obj['id'] == 3:
        #     return self.fire_interaction(entity, obj)
        else:
            return f"Interacted with a {obj['name']}"


    def tree_interaction(self, entity, tree):
        required_level = (tree['tier'] * 10) - 10
        if entity.skills.get_level('woodcutting') >= required_level:
            entity.skills.add_xp('woodcutting', (tree['tier'] * 10))
            # self.grid.get_tile(entity.x, entity.y).remove('object')
            return f"Chopped down a {tree['name']}."
        else:
            return f"Your woodcutting level is too low to chop down this {tree['name']}."

    def rock_interaction(self, entity, rock):
        required_level = (rock['tier'] * 10) - 10
        if entity.skills.get_level('mining') >= required_level:
            entity.skills.add_xp('mining', (rock['tier'] * 10 ))

            return f"Mined a {rock['name']}."
        else:
            return f"Your mining level is too low to mine this {rock['name']}."

    def fire_interaction(self, entity, fire):
        required_level = fire['tier'] * 10
        if entity.skills.get_level('firemaking') >= required_level:
            entity.skills.add_xp('firemaking', (fire['tier'] * 10))
            return f"Used the {fire['name']} for firemaking."
        else:
            return f"Your firemaking level is too low to use this {fire['name']}."


