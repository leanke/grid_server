import json
from grid_server.classes.items.item import Item
from grid_server.classes.items.weapons import Weapon
from grid_server.classes.items.armor import Armor
from grid_server.classes.items.resources import Resource

class Skills:
    def __init__(self):
        self.skills = {
            'attack': {'level': 1, 'xp': 0},
            'strength': {'level': 1, 'xp': 0},
            'defence': {'level': 1, 'xp': 0},
            'health': {'level': 3, 'xp': 0},
            'magic': {'level': 1, 'xp': 0},
            'ranged': {'level': 1, 'xp': 0},
            'woodcutting': {'level': 1, 'xp': 0},
            'mining': {'level': 1, 'xp': 0},
            'firemaking': {'level': 1, 'xp': 0}
        }

    def to_dict(self):
        return self.skills

    def add_xp(self, skill, amount):
        if skill in self.skills:
            self.skills[skill]['xp'] += amount
            self.check_level_up(skill)

    def check_level_up(self, skill):
        level_up_threshold = 100 * (self.skills[skill]['level'] ** 1.5)
        while self.skills[skill]['xp'] >= level_up_threshold:
            self.skills[skill]['xp'] -= level_up_threshold
            self.skills[skill]['level'] += 1

    def get_level(self, skill):
        return self.skills[skill]['level'] if skill in self.skills else 0

    def can_use(self, skill, item_level):
        return self.get_level(skill) >= item_level

    def combat_level(self):
        combat_skills = ['attack', 'strength', 'defence', 'health', 'magic', 'ranged']
        lvl_sum = 0
        for skill in combat_skills:
            for k, v in self.skills[skill].items():
                if k == skill:
                    lvl_sum += v['level']
        #     print(skill)
        #     print()
        #     skill_level = self.get_level(skill)
        #     lvl_sum += skill_level
        # print(lvl_sum // len(combat_skills))
        return lvl_sum // len(combat_skills)
    
    def set_level(self, skill, level):
        self.skills[skill]['xp'] = 100 * (level ** 1.5)
        self.skills[skill]['level'] = level

    def to_dict(self):
        return self.skills

class Inventory:
    def __init__(self):
        self.slots = [{} for _ in range(9)]
        self.equipped = {
            'head': {},
            'body': {},
            'gloves': {},
            'legs': {},
            'boots': {},
            'left_hand': {},
            'right_hand': {},
            'cape': {},
            'ring': {},
            'amulet': {},
            'arrow': {},
        }

    def to_dict(self):
        return {
            'slots': self.slots,
            'equipped': self.equipped
        }

    def add(self, item):
        item_dict = item.to_dict() if isinstance(item, Item) else item
        for slot in self.slots:
            if slot:
                if slot['name'] == item_dict['name'] and item_dict['stackable']:
                    slot['quantity'] += item_dict['quantity']
                    return True
        for i, slot in enumerate(self.slots):
            if not slot:
                self.slots[i] = item_dict
                return True
        return False

    def drop(self, item_name):
        for slot in self.slots:
            if slot and slot['name'] == item_name:
                dropped = slot.copy()
                slot.clear()
                if 'damage' in dropped:
                    return Weapon(**dropped)
                elif 'armor' in dropped:
                    return Armor(**dropped)
                else:
                    return Resource(**dropped)
        return None

    def use(self, item_name):
        for slot in self.slots:
            if slot and slot['name'] == item_name:
                if slot['quantity'] > 1:
                    slot['quantity'] -= 1
                else:
                    slot.clear()
                return True
        return False

    def can_equip(self, item):
        if not isinstance(item, Weapon) and not isinstance(item, Armor):
            return False, None
        for key in self.equipped.keys():
            if item.slot.lower() in key:
                return True, key
        return False, None

    def equip(self, item):
        can_equip, equip_slot = self.can_equip(item)
        if can_equip:
            if self.equipped[equip_slot] is {} and 'damage' in item:
                self.add(Weapon(**self.equipped[equip_slot]))
                self.equipped[equip_slot] = item.to_dict()
            elif self.equipped[equip_slot] is {} and 'armor' in item:
                self.add(Armor(**self.equipped[equip_slot]))
                self.equipped[equip_slot] = item.to_dict()
            return True

    def unequip(self, equip_slot):
        if equip_slot in self.equipped and self.equipped[equip_slot] is not {}:
            item = self.equipped[equip_slot]
            if 'damage' in item:
                self.add(Weapon(**item))
                self.equipped[equip_slot] = item.to_dict()
            elif 'armor' in item:
                self.add(Armor(**item))
                self.equipped[equip_slot] = item.to_dict()
            self.add(Item(**item))
            self.equipped[equip_slot] = {}
            return True
        return False
    
    def drop_inventory(self):
        drop = []
        for slot in self.slots:
            if slot:
                if slot != {}:
                    drop.append(slot.copy())
                    slot.clear()
        for slot, item in self.equipped.items():
            if slot != {}:
                drop.append(item.copy())
                item.clear()
        if len(drop) > 0:
            return drop
        else:
            return None

class Entity:
    def __init__(self, coords, id, name, pid=None):
        self.id = id
        self.name = name
        self.pid = pid
        self.x = coords[0]
        self.y = coords[1]
        self.home = coords
        self.direction = 'up'
        self.skills = Skills()
        self.max_health = self.skills.get_level('health') * 5
        self.health = self.max_health
        self.combat_level = self.skills.combat_level()
        self.inventory = Inventory()

    def entity_data(self):
        data = {
            'id': self.id,
            'pid': self.pid,
            'name': self.name,
            'type': self.__class__.__name__.lower(),
            'health': self.health,
            'combat_level': self.combat_level,
            'skills': self.skills.to_dict(),
            'inventory': self.inventory.to_dict()
        }
        return data

    # Items
    def pick_up(self, item):
        if isinstance(item, Item):
            self.inventory.add(item)
        else:
            self.inventory.add(Item(**item))

    def drop(self, item):
        return self.inventory.drop(item)

    def use(self, item):
        return self.inventory.use(item)

    def equip(self, item):
        return self.inventory.equip(item)

    def unequip(self, equip_slot):
        return self.inventory.unequip(equip_slot)

    # Combat
    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.die()
            return True, self.die()
        return False, []

    def die(self):
        drops = self.inventory.drop_inventory()
        self.health = self.max_health
        setattr(self, 'x', self.home[0])
        setattr(self, 'y', self.home[1])
        return drops
    
    def get_weapon_type(self):
        left = None
        right = None
        if self.inventory.equipped['left_hand']:
            left = self.inventory.equipped['left_hand']['type']
        if self.inventory.equipped['right_hand']:
            right = self.inventory.equipped['right_hand']['type']
        return left, right

    def attack(self):
        left, right = self.get_weapon_type()
        left_damage, right_damage = self.damage_calc()
        targets_damage = {'left':{'damage': left_damage, 'target': []}, 'right':{'damage': right_damage, 'target': []}}
        left_tiles = []
        right_tiles = []
        if left is not None and left_damage > 0:
            targets_damage['left']['damage'] = left_damage
            if left == 'melee':
                tile = self.get_target_tile()
                left_tiles.append(tile)
            elif left == 'range':
                tiles = self.get_line_of_tiles(3)
                left_tiles.append(tiles)
            elif left == 'magic':
                tiles = self.get_area_of_tiles(3)
                left_tiles.append(tiles)
        else:
            tile = self.get_target_tile()
            left_tiles.append(tile)
        if right is not None and right_damage > 0:
            targets_damage['right']['damage'] = right_damage
            if right == 'melee':
                tile = self.get_target_tile()
                right_tiles.append(tile)
            elif right == 'range':
                tiles = self.get_line_of_tiles(3)
                right_tiles.append(tiles)
            elif right == 'magic':
                tiles = self.get_area_of_tiles(3)
                right_tiles.append(tiles)
        else:
            tile = self.get_target_tile()
            right_tiles.append(tile)
        targets_damage['left']['target'] = left_tiles
        targets_damage['right']['target'] = right_tiles
        return targets_damage
        
    def damage_calc(self):
        right_damage = 1
        left_damage = 1
        if self.inventory.equipped['left_hand']:
            left = self.inventory.equipped['left_hand']
            if left['type'] == 'melee':
                left_damage += ((self.skills.get_level('attack') + self.skills.get_level('strength')) // 2) + left['damage']
            if left['type'] == 'magic':
                left_damage += self.skills.get_level('magic') + left['damage']
            if left['type'] == 'range':
                left_damage += self.skills.get_level('range') + left['damage']
        if self.inventory.equipped['right_hand']:
            right = self.inventory.equipped['right_hand']
            if right['type'] == 'melee':
                right_damage += ((self.skills.get_level('attack') + self.skills.get_level('strength')) // 2) + right['damage']
            if right['type'] == 'magic':
                right_damage += self.skills.get_level('magic') + right['damage']
            if right['type'] == 'range':
                right_damage += self.skills.get_level('range') + right['damage']
        return left_damage, right_damage
    
    def combat_xp(self, combat_style):
        if combat_style == 'melee':
            self.skills.add_xp('attack', 10)
            self.skills.add_xp('strength', 10)
        if combat_style == 'magic':
            self.skills.add_xp('magic', 10)
        if combat_style == 'range':
            self.skills.add_xp('range', 10)

    # Target Tiles
    def get_target_tile(self, offset_x=0, offset_y=0):
        x, y = self.x + offset_x, self.y + offset_y
        if self.direction == 'up':
            x -= 1
        elif self.direction == 'down':
            x += 1
        elif self.direction == 'left':
            y -= 1
        elif self.direction == 'right':
            y += 1
        return (x, y)

    def get_line_of_tiles(self, length):
        tiles = []
        x, y = self.x, self.y
        for _ in range(length):
            x, y = self.get_target_tile()
            tiles.append((x, y))
        return tiles

    def get_area_of_tiles(self, size):
        tiles = []
        half_size = size // 2
        for dx in range(-half_size, half_size + 1):
            for dy in range(-half_size, half_size + 1):
                tiles.append((self.x + dx, self.y + dy))
        return tiles


    def client_data(self):
        data = {
        'rank': self.rank,
        'title': self.title,
        'type': self.type,
        'x': self.x,
        'y': self.y,
        'local_x': self.local_x,
        'local_y': self.local_y,
        'direction': self.direction,
        'skills': self.skills.to_dict(),
        'inventory': self.inventory.to_dict(),
        'id': self.id,
        'name': self.name,
        'pid': self.pid,
        'home': self.home,
        'direction': self.direction,
        'max_health': self.max_health,
        'health': self.health,
        'combat_level': self.skills.combat_level(),
        }
        return data
    
    def save(self):
        save_data = {
            'base': {'pid': self.pid, 'name': self.name, 'password': self.password, 'rank': self.rank, 'title': self.title, 'type': self.type},
            'stats': {'x': self.x, 'y': self.y, 'direction': self.direction, 'total_time': self.total_time},
            'client': {'x': self.local_x, 'y': self.local_y},
            'skills': self.skills.to_dict(),
            'health': self.health,
            'inventory': self.inventory.to_dict()
        }
        with open(self.path, 'w') as f:
            json.dump(save_data, f, indent=4)

