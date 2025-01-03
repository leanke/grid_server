import json

class Player:
    def __init__(self, json_file, path):
        self.path = path + '.json'
        self.name = json_file['base']['name']
        self.password = json_file['base']['password']
        self.id = json_file['base']['id']
        self.rank = json_file['base']['rank']
        self.title = json_file['base']['title']
        self.type = json_file['base']['type']
        self.x = json_file['stats']['x']
        self.y = json_file['stats']['y']
        self.direction = json_file['stats']['direction']
        self.total_time = json_file['stats']['total_time']
        self.skills = json_file['skills']
        self.xp = json_file['xp']  # Initialize XP for each skill
        self.inventory = json_file['inventory']  # Initialize empty inventory

    def save(self):
        save_data = {
            'base': {'id': self.id, 'name': self.name, 'password': self.password, 'rank': self.rank, 'title': self.title, 'type': self.type},
            'stats': {'x': self.x, 'y': self.y, 'direction': self.direction, 'total_time': self.total_time},
            'skills': self.skills,
            'xp': self.xp,  # Save XP data
            'inventory': self.inventory  # Save inventory data
        }
        with open(self.path, 'w') as f:
            json.dump(save_data, f)

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
        level_up_threshold = 100  # Example threshold for leveling up
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
