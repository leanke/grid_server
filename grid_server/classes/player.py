import json

class Player:
    def __init__(self, player, path):
        self.path = path + '.json'
        self.name = player['base']['name']
        self.password = player['base']['password']
        self.pid = player['base']['pid']
        self.rank = player['base']['rank']
        self.title = player['base']['title']
        self.type = player['base']['type']
        self.x = player['stats']['x']
        self.y = player['stats']['y']
        self.direction = player['stats']['direction']
        self.total_time = player['stats']['total_time']
        self.skills = player['skills']
        self.xp = player['xp']
        self.inventory = player['inventory']
        self.max_health = self.skills['health'] * 10
        self.current_health = self.max_health
        self.combat_level = (self.skills['attack'] + self.skills['defence'] + self.skills['health']) // 3

    def player_data(self):
        data = {
            'base': {'id': self.pid, 'name': self.name, 'type': self.type},
            'coords': {'x': self.x, 'y': self.y},
            'direction': self.direction,
            'skills': self.skills,
            'xp': self.xp,
            'max_health': self.max_health,
            'health': self.current_health,
            'inventory': self.inventory,
            'combat_level': self.combat_level
        }
        return data
    
    def save(self):
        save_data = {
            'base': {'pid': self.pid, 'name': self.name, 'password': self.password, 'rank': self.rank, 'title': self.title, 'type': self.type},
            'stats': {'x': self.x, 'y': self.y, 'direction': self.direction, 'total_time': self.total_time},
            'skills': self.skills,
            'xp': self.xp,
            'health': self.current_health,
            'inventory': self.inventory
        }
        with open(self.path, 'w') as f:
            json.dump(save_data, f, indent=4)

    def info(self):
        string = (
            f"Info: {self.name}\n" +
            f"    Attack: {self.skills['attack']}, Defence: {self.skills['defence']}, Health: {self.skills['health']}\n" +
            f"    Woodcutting: {self.skills['woodcutting']}, Mining: {self.skills['mining']}, Firemaking: {self.skills['firemaking']}\n"
        )
        return string

    def add_xp(self, skill, amount):
        if skill in self.skills:
            self.xp[skill] += amount
            self.check_level_up(skill)

    def check_level_up(self, skill):
        level_up_threshold = 100
        while self.xp[skill] >= level_up_threshold:
            self.xp[skill] -= level_up_threshold
            self.skills[skill] += 1
            print(f"{self.name} leveled up in {skill}! New level: {self.skills[skill]}")

    def add_item(self, item):
        if len(self.inventory) < 24:
            self.inventory.append(item)
            print(f"Added {item} to inventory.")
        else:
            print("Inventory is full. Cannot add more items.")

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"Removed {item} from inventory.")
        else:
            print(f"{item} not found in inventory.")
    