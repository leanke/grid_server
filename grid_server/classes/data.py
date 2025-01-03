import numpy as np

# ID Scheme
# 0: 'empty',
# 1 - 999: 'debug',
# 1,000 - 999,999: 'game_objects'
# 1,000,000 - 1,999,999: 'players'

item_ids = {
    1: { # sword
        'id': 1,
        'name': 'Sword',
        'description': 'A sharp sword',
        'level': 1,
        'value': 20,
        'damage': 1
    },
    2: { # shield
        'id': 2,
        'name': 'Shield',
        'description': 'A strong shield',
        'level': 1,
        'value': 15,
        'defense': 1
    },
    3: { # staff
        'id': 3,
        'name': 'Staff',
        'description': 'A Staff',
        'level': 1,
        'value': 20,
        'damage': 1
    },
    4: { # bow
        'id': 4,
        'name': 'Bow',
        'description': 'A Bow',
        'level': 1,
        'value': 20,
        'damage': 1
    },
    5: { # arrow
        'id': 5,
        'name': 'Arrow',
        'description': 'An Arrow',
        'level': 1,
        'value': 1,
        'damage': 1
    },
    6: { # pick axe
        'id': 6,
        'name': 'Pick Axe',
        'description': 'A Pick Axe',
        'level': 1,
        'value': 20,
        'damage': 1
    },
    7: { # axe
        'id': 7,
        'name': 'Axe',
        'description': 'An Axe',
        'level': 1,
        'value': 20,
        'damage': 1
    },
}

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

objects = [
{'obj_id': 1, 'coords': (5,14), 'attr': {'type': 'tree', 'health': 5, 'mod': None, 'resource': 'logs'}},
{'obj_id': 2, 'coords': (5,16), 'attr': {'type': 'rock', 'health': 10, 'mod': None, 'resource': 'stone'}},
{'obj_id': 2, 'coords': (7,1), 'attr': {'type': 'rock', 'health': 10, 'mod': 'tin', 'resource': 'tin ore'}},
{'obj_id': 2, 'coords': (8,16), 'attr': {'type': 'rock', 'health': 10, 'mod': 'copper', 'resource': 'copper ore'}},
{'obj_id': 1, 'coords': (9,14), 'attr': {'type': 'tree', 'health': 10, 'mod': 'oak', 'resource': 'oak logs'}},
{'obj_id': 1, 'coords': (12,3), 'attr': {'type': 'tree', 'health': 10, 'mod': 'oak', 'resource': 'oak logs'}},
{'obj_id': 1, 'coords': (12,9), 'attr': {'type': 'tree', 'health': 15, 'mod': 'willow', 'resource': 'willow logs'}},
{'obj_id': 1, 'coords': (13,5), 'attr': {'type': 'tree', 'health': 15, 'mod': 'willow', 'resource': 'willow logs'}},
{'obj_id': 2, 'coords': (14,9), 'attr': {'type': 'rock', 'health': 10, 'mod': None, 'resource': 'stone'}},
{'obj_id': 1, 'coords': (14,12), 'attr': {'type': 'tree', 'health': 5, 'mod': None, 'resource': 'logs'}},
{'obj_id': 1, 'coords': (15,7), 'attr': {'type': 'tree', 'health': 5, 'mod': None, 'resource': 'logs'}},
]