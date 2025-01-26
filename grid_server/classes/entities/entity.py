import json
from grid_server.classes.items.item import Item
from grid_server.classes.items.weapons import Weapon
from grid_server.classes.items.armor import Armor
from grid_server.classes.items.resources import Resource
from grid_server.classes.objects.bank import Bank

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
            lvl_sum += self.skills[skill]['level']
        return lvl_sum // len(combat_skills)
    
    def set_level(self, skill, level):
        self.skills[skill]['xp'] = 100 * (level ** 1.5)
        self.skills[skill]['level'] = level

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
            'arrow': {},
        }

    def to_dict(self):
        return {
            'slots': self.slots,
            'equipped': self.equipped
        }

    def add(self, item):
        if 'quantity' not in item or item['quantity'] == 0:
            item['quantity'] = 1
        for slot in self.slots:
            if slot != {}:
                if slot['name'] == item['name'] and item['stackable']:
                    slot['quantity'] += item['quantity']
                    return True
        for i, slot in enumerate(self.slots):
            if not slot:
                self.slots[i] = item
                return True
        return False

    def drop(self, slot):
        if 0 <= slot < len(self.slots):
            dropped = self.slots[slot]
            self.slots[slot] = {}
            if dropped:
                return dropped

    def use(self, slot):
        if 0 <= slot < len(self.slots) and self.slots[slot] != {}:
            item = self.slots[slot]
            can_eq, equip_slot = self.can_equip(item)
            if can_eq:
                self.equip(item, equip_slot)
                self.slots[slot] = {}
                return True
            if 'food' in item:
                return self.eat(item)
        return False

    def can_equip(self, item):
        if 'damage' in item or 'armor' in item:
            equip_slot = item['slot']
            return True, equip_slot
        else:
            return False, None

    def equip(self, item, slot):
            if slot in self.equipped and self.equipped[slot] == {}:
                self.equipped[slot] = item
            elif slot in self.equipped and self.equipped[slot] != {}:
                old_item = self.equipped[slot]
                self.add(old_item)
                self.equipped[slot] = item
            return True

    def unequip(self, slot):
        if slot in self.equipped and self.equipped[slot] is not {}:
            item = self.equipped[slot]
            self.add(item)
            self.equipped[slot] = {}
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
        self.x, self.y = coords
        self.home = coords
        self.direction = 'up'
        self.skills = Skills()
        self.max_health = self.skills.get_level('health') * 5
        self.health = self.max_health
        self.combat_level = self.skills.combat_level()
        self.inventory = Inventory()
        self.bank = Bank()

    def entity_data(self):
        return {
            'id': self.id,
            'pid': self.pid,
            'name': self.name,
            'type': self.__class__.__name__.lower(),
            'health': self.health,
            'combat_level': self.combat_level,
            'skills': self.skills.to_dict(),
            'inventory': self.inventory.to_dict(),
            'bank': self.bank.to_dict()
        }

    def pick_up(self, item):
        self.inventory.add(item)

    def drop(self, item):
        return self.inventory.drop(item)

    def use(self, slot):
        return self.inventory.use(slot)

    def equip(self, item):
        return self.inventory.equip(item)

    def unequip(self, equip_slot):
        return self.inventory.unequip(equip_slot)

    def receive_damage(self, damage):
        self.health = max(self.health - damage, 0)
        self.skills.add_xp('defense', damage)
        if self.health == 0:
            return True, self.die()
        return False, []

    def die(self):
        drops = self.inventory.drop_inventory()
        self.health = self.max_health
        self.x, self.y = self.home
        return drops
    
    def get_weapon_type(self):
        left = self.inventory.equipped['left_hand'].get('type') if self.inventory.equipped['left_hand'] != {} else None
        right = self.inventory.equipped['right_hand'].get('type') if self.inventory.equipped['right_hand'] != {} else None
        return left, right

    def attack(self):
        left, right = self.get_weapon_type()
        self.combat_xp(left)
        self.combat_xp(right)
        left_damage, right_damage = self.damage_calc()
        targets_damage = {
            'left': {'damage': left_damage, 'target': []}, 
            'right': {'damage': right_damage, 'target': []}
            }
        targets_damage['left']['target'] = self.get_attack_tiles(left, left_damage)
        targets_damage['right']['target'] = self.get_attack_tiles(right, right_damage)
        return targets_damage

    def get_attack_tiles(self, weapon_type, damage):
        if weapon_type is not None:
            if weapon_type == 'melee':
                return [self.get_target_tile()]
            elif weapon_type == 'range':
                return self.get_line_of_tiles(3)
            elif weapon_type == 'magic':
                return self.get_area_of_tiles(3)
        else:
            return [self.get_target_tile()]

    def damage_calc(self):
        left_damage = self.calculate_hand_damage(self.inventory.equipped['left_hand'])
        right_damage = self.calculate_hand_damage(self.inventory.equipped['right_hand'])
        return left_damage, right_damage

    def calculate_hand_damage(self, hand):
        if not hand:
            return 1
        base_damage = 1
        if hand['type'] == 'melee':
            base_damage += ((self.skills.get_level('attack') + self.skills.get_level('strength')) // 2) + hand['damage']
        elif hand['type'] == 'magic':
            base_damage += self.skills.get_level('magic') + hand['damage']
        elif hand['type'] == 'range':
            base_damage += self.skills.get_level('range') + hand['damage']
        return base_damage
    
    def combat_xp(self, combat_style):
        health_level = self.skills.get_level('health')
        xp_map = {'melee': ['attack', 'strength'], 'magic': ['magic'], 'range': ['range']}
        self.skills.add_xp('health', 3)
        new_health_level = self.skills.get_level('health')
        if new_health_level > health_level:
            self.max_health = new_health_level * 5
            self.health += 5
        for skill in xp_map.get(combat_style, []):
            self.skills.add_xp(skill, 10)

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
        if self.direction == 'up':
            return [(self.x - i, self.y) for i in range(length)]
        elif self.direction == 'down':
            return [(self.x + i, self.y) for i in range(length)]
        elif self.direction == 'left':
            return [(self.x, self.y - i) for i in range(length)]
        elif self.direction == 'right':
            return [(self.x, self.y + i) for i in range(length)]

    def get_area_of_tiles(self, size):
        half_size = size // 2
        coord_list = []
        for dx in range(-half_size, half_size + 1):
            for dy in range(-half_size, half_size + 1):
                coord_list.append((self.x + dx, self.y + dy))
        return coord_list

    def client_data(self):
        return {
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
            'max_health': self.max_health,
            'health': self.health,
            'combat_level': self.skills.combat_level(),
        }
    
    def save(self):
        save_data = {
            'base': {'pid': self.pid, 'name': self.name, 'password': self.password, 'rank': self.rank, 'title': self.title, 'type': self.type},
            'stats': {'x': self.x, 'y': self.y, 'direction': self.direction, 'total_time': self.total_time},
            'client': {'x': self.local_x, 'y': self.local_y},
            'skills': self.skills.to_dict(),
            'health': self.health,
            'inventory': self.inventory.to_dict(),
            'bank': self.bank.to_dict()
        }
        with open(self.path, 'w') as f:
            json.dump(save_data, f, indent=4)

    def deposit_to_bank(self, item):
        return self.bank.add(item)

    def withdraw_from_bank(self, slot):
        return self.bank.remove(slot)



