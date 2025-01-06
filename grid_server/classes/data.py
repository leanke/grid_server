import numpy as np
from grid_server.classes.objects import GameObject
from grid_server.classes.items import Item
from grid_server.classes.npc import NPC
from grid_server.classes.tile import Tile

# ID Scheme
# 0: 'empty',
# 1 - 999: 'debug',
# 1,000 - 999,999: 'game_objects'
# 1,000,000 - 1,999,999: 'players'


trees = {
    1: GameObject.create_tree(1, 5, 'logs').__dict__,
    2: GameObject.create_tree(2, 10, 'oak logs').__dict__,
    3: GameObject.create_tree(3, 15, 'willow logs').__dict__,
    4: GameObject.create_tree(4, 20, 'maple logs').__dict__,
}   

rocks = {
    1: GameObject.create_rock(1, 10, 'stone').__dict__,
    2: GameObject.create_rock(2, 10, 'tin ore').__dict__,
    3: GameObject.create_rock(3, 10, 'copper ore').__dict__,
    4: GameObject.create_rock(4, 10, 'iron ore').__dict__,
}

walls = {
    1: GameObject.create_wall(1, 100, 'wall').__dict__,
}

swords = {
    1: Item.create_sword(1).__dict__,
    2: Item.create_sword(2).__dict__,
    3: Item.create_sword(3).__dict__,
    4: Item.create_sword(4).__dict__,
}

shields = {
    1: Item.create_shield(1).__dict__,
    2: Item.create_shield(2).__dict__,
    3: Item.create_shield(3).__dict__,
    4: Item.create_shield(4).__dict__,
}

staffs = {
    1: Item.create_staff(1).__dict__,
    2: Item.create_staff(2).__dict__,
    3: Item.create_staff(3).__dict__,
    4: Item.create_staff(4).__dict__,
}

bows = {
    1: Item.create_bow(1).__dict__,
    2: Item.create_bow(2).__dict__,
    3: Item.create_bow(3).__dict__,
    4: Item.create_bow(4).__dict__,
}



item_ids = {
    1: Item.create_sword(1).__dict__,
    2: Item.create_shield(1).__dict__,
    3: Item.create_staff(1).__dict__,
    4: Item.create_bow(1).__dict__,
    5: Item.create_item(5, 'Arrow', 'An Arrow', 1).__dict__,
    6: Item.create_item(6, 'Pick Axe', 'A Pick Axe', 1).__dict__,
    7: Item.create_item(7, 'Axe', 'An Axe', 1).__dict__,
}

sample_entity = {
    'entity': {
        1: NPC.create_npc(1, 1, 'Man', 'npc', 2, 10).__dict__,
        2: NPC.create_npc(2, 2, 'Goblin', 'npc', 1, 10).__dict__,
        # Player entity will be created dynamically
    },
}

tile_objects = {
    0: Tile(None, None, None).__dict__,
    1: Tile(trees[1], None, None).__dict__,
    2: GameObject(2, 'Rock', 'A Rock', None, None, None).__dict__,
    3: GameObject(3, 'Player', 'A Player', None, None, None).__dict__,
    4: GameObject(4, 'Wall', 'A Wall', 1, 100, 'wall').__dict__,
    5: GameObject(5, 'Sword', 'A Sword', None, None, None).__dict__,
    6: GameObject(6, 'Axe', 'An Axe', None, None, None).__dict__,
    7: GameObject(7, 'Staff', 'A Staff', None, None, None).__dict__,
    8: GameObject(8, 'Bow', 'A Bow', None, None, None).__dict__,
    9: GameObject(9, 'Arrow', 'An Arrow', None, None, None).__dict__,
}
objects_placed = [
{'coords': (5,14), 'data': trees[1]},
{'coords': (5,16), 'data': rocks[1]},
{'coords': (7,1), 'data': rocks[2]},
{'coords': (8,16), 'data': rocks[3]},
{'coords': (9,14), 'data': trees[2]},
{'coords': (12,3), 'data': trees[2]},
{'coords': (12,9), 'data': trees[3]},
{'coords': (13,5), 'data': trees[4]},
{'coords': (14,9), 'data': rocks[4]},
{'coords': (14,12), 'data': trees[1]},
{'coords': (15,7), 'data': trees[1]},
]

objects_debug = [
    # Trees
{'coords': (5,5), 'data': trees[1]},
{'coords': (5,6), 'data': trees[1]},
{'coords': (6,5), 'data': trees[1]},
{'coords': (6,6), 'data': trees[1]},

{'coords': (5,7), 'data': trees[2]},
{'coords': (5,8), 'data': trees[2]},
{'coords': (6,7), 'data': trees[2]},
{'coords': (6,8), 'data': trees[2]},

{'coords': (5,9), 'data': trees[3]},
{'coords': (5,10), 'data': trees[3]},
{'coords': (6,9), 'data': trees[3]},
{'coords': (6,10), 'data': trees[3]},

{'coords': (5,11), 'data': trees[4]},
{'coords': (5,12), 'data': trees[4]},
{'coords': (6,11), 'data': trees[4]},
{'coords': (6,12), 'data': trees[4]},

    # rocks
{'coords': (9,5), 'data': rocks[1]},
{'coords': (9,6), 'data': rocks[1]},
{'coords': (10,5), 'data': rocks[1]},
{'coords': (10,6), 'data': rocks[1]},

{'coords': (9,7), 'data': rocks[2]},
{'coords': (9,8), 'data': rocks[2]},
{'coords': (10,7), 'data': rocks[2]},
{'coords': (10,8), 'data': rocks[2]},

{'coords': (9,9), 'data': rocks[3]},
{'coords': (9,10), 'data': rocks[3]},
{'coords': (10,9), 'data': rocks[3]},
{'coords': (10,10), 'data': rocks[3]},

{'coords': (9,11), 'data': rocks[4]},
{'coords': (9,12), 'data': rocks[4]},
{'coords': (10,11), 'data': rocks[4]},
{'coords': (10,12), 'data': rocks[4]},
]


object_ids = {
0: 'empty',
1: 'tree',
2: 'rock',
3: 'player',
4: 'wall',
5: 'PlaceHolder5',
6: 'PlaceHolder6',
7: 'PlaceHolder7',
8: 'PlaceHolder8',
9: 'PlaceHolder9',
10: 'rock',
11: 'rock11',
12: 'rock12',
13: 'rock13',
14: 'rock14',
15: 'rock15',
16: 'rock16',
17: 'rock17',
18: 'rock18',
19: 'rock19',
20: 'tree',
21: 'oak_tree',
22: 'willow_tree',
23: 'maple_tree',
24: 'tree24',
25: 'tree25',
26: 'tree26',
27: 'tree27',
28: 'tree28',
29: 'tree29',
}

RENDERING_ID = {
    'tbu': f'֍֎۩۝۞ѺѺ҈҉⌂●○◌◊﴾﴿',
    "up": '▲',
    "down": '▼',
    "left": '◄',
    "right": '►',
    0: '.',
    1: 'T',
    2: 'R',
    3: 'P',
    4: '█',
    5: '?',
    20: 'T'
}



# data = {
#     'player': {
#             'id': 3,
#             'pid': player.pid,
#             'name': player.name,
#             'type': player.type,
#             'coords': {'x': player.x, 'y': player.y},
#             'direction': player.direction,
#             'skills': player.skills,
#             'xp': player.xp,
#             'max_health': player.max_health,
#             'health': player.current_health,
#             'inventory': player.inventory,
#             'combat_level': player.combat_level
#         },
#     'array': self.grid_world.grid.client_view(player.x, player.y),
#     'text': self.grid_world.step(action, player),
# }




tile_sample = {
            'tile_id': int, # should be the object_id befor anything else
            'tile': {
                'object': {
                        'id': int, 
                        'name': str,
                        'description': str,
                        'tier': int, 
                        'health': int, 
                        'resource': str
                        },
                'entity': {
                        'id': int,
                        'pid': int,
                        'name': str,
                        'type': str,
                        'health': int,
                        'combat_level': int
                        },
                'item':{
                        'id': int,
                        'name': str,
                        'description': str,
                        'item_type': str,
                        'level': int,
                        'value': int,
                        'damage': int,
                        'defense': int,
                        },
                    }
                }




