import json
from grid_server.classes.entities.entity import Entity, Inventory, Skills

class Player(Entity):
    def __init__(self, player, path):
        super().__init__((player['stats']['x'], player['stats']['y']), 1, player['base']['name'], pid=player['base']['pid'])
        if path is None:
            self.path = f'./grid_server/users/{self.name}'
            
        self.path = path + '.json'
        self.password = player['base']['password']
        self.rank = player['base']['rank']
        self.title = player['base']['title']
        self.type = player['base']['type']
        self.x = player['stats']['x']
        self.y = player['stats']['y']
        self.local_x = player['client']['x']
        self.local_y = player['client']['y']
        self.direction = player['stats']['direction']
        self.total_time = player['stats']['total_time']
        self.skills = Skills()
        for skill, data in player['skills'].items():
            self.skills.skills[skill] = data
        self.inventory = Inventory()
        for item in player['inventory']['slots']:#['slots']:
            if item != {}:
                self.inventory.add(item)
        for slot, item in player['inventory']['equipped'].items():
            self.inventory.equip(item, slot)
        self.menu_drop = False

    def client_data(self):
        data = super().client_data()
        data['menu_drop'] = self.menu_drop
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

    def add_xp(self, skill, amount):
        self.skills.add_xp(skill, amount)

    def check_level_up(self, skill):
        self.skills.check_level_up(skill)

    def menu(self, action):
        if self.menu_drop:
            return self.drop(action)
        





    # def create_player(self, username, password):
    #     new_player = {
    #         "base": {
    #             "pid": f'{str(uuid.uuid4())[:4]}', 
    #             "name": f'{str(username)}', 
    #             "password": f'{str(password)}', 
    #             "rank": 1, 
    #             "title": "None", 
    #             "type": "None"
    #         },
    #         "stats": {
    #             "x": 2, 
    #             "y": 2, 
    #             "direction": "left", 
    #             "total_time": 0
    #         },
    #         "client": {"x": 14, "y": 14},
    #         "skills": {
    #             "attack": {"level": 1, "xp": 0}, 
    #             "strength": {"level": 1, "xp": 0}, 
    #             "defence": {"level": 1, "xp": 0}, 
    #             "health": {"level": 3, "xp": 0}, 
    #             "magic": {"level": 1, "xp": 0}, 
    #             "ranged": {"level": 1, "xp": 0}, 
    #             "woodcutting": {"level": 1, "xp": 0}, 
    #             "mining": {"level": 1, "xp": 0}, 
    #             "firemaking": {"level": 1, "xp": 0}},
    #         "health":  10,
    #         "inventory": []
    #         }
    #     return new_player