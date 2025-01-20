
from grid_server.classes.tile import Tile
from grid_server.classes.objects.object_data import trees, rocks, walls
from grid_server.classes.items.item_data import items
# from grid_server.classes.entities.entity_data import entities
from grid_server.classes.entities.npc import Mage, Warrior, Archer



tile_objects = {
    'empty': Tile(None, None, None).__dict__,
    'tree': Tile(trees[1], None, None).__dict__,
    'rock': Tile(rocks[1], None, None).__dict__,
    'wall': Tile(walls[1], None, None)
}

objects_debug = [
    # Trees
    {'coords': (15,1), 'data': trees[1]},
    {'coords': (16,1), 'data': trees[1]},
    {'coords': (15,2), 'data': trees[1]},
    {'coords': (16,2), 'data': trees[1]},

    {'coords': (15,3), 'data': trees[2]},
    {'coords': (16,3), 'data': trees[2]},
    {'coords': (15,4), 'data': trees[2]},
    {'coords': (16,4), 'data': trees[2]},

    {'coords': (15,5), 'data': trees[3]},
    {'coords': (16,5), 'data': trees[3]},
    {'coords': (15,6), 'data': trees[3]},
    {'coords': (16,6), 'data': trees[3]},

    {'coords': (15,7), 'data': trees[4]},
    {'coords': (16,7), 'data': trees[4]},
    {'coords': (15,8), 'data': trees[4]},
    {'coords': (16,8), 'data': trees[4]},

    {'coords': (15,9), 'data': trees[5]},
    {'coords': (16,9), 'data': trees[5]},

    {'coords': (15,10), 'data': trees[6]},
    {'coords': (16,10), 'data': trees[6]},

    {'coords': (15,11), 'data': trees[7]},
    {'coords': (16,11), 'data': trees[7]},

    {'coords': (15,12), 'data': trees[8]},
    {'coords': (16,12), 'data': trees[8]},

    # rocks
    {'coords': (1,15), 'data': rocks[1]},
    {'coords': (1,16), 'data': rocks[1]},
    {'coords': (2,15), 'data': rocks[1]},
    {'coords': (2,16), 'data': rocks[1]},

    {'coords': (3,15), 'data': rocks[2]},
    {'coords': (3,16), 'data': rocks[2]},
    {'coords': (4,15), 'data': rocks[2]},
    {'coords': (4,16), 'data': rocks[2]},

    {'coords': (5,15), 'data': rocks[3]},
    {'coords': (5,16), 'data': rocks[3]},
    {'coords': (6,15), 'data': rocks[3]},
    {'coords': (6,16), 'data': rocks[3]},

    {'coords': (7,15), 'data': rocks[4]},
    {'coords': (7,16), 'data': rocks[4]},
    {'coords': (8,15), 'data': rocks[4]},
    {'coords': (8,16), 'data': rocks[4]},

    {'coords': (9,15), 'data': rocks[5]},
    {'coords': (9,16), 'data': rocks[5]},

    {'coords': (10,15), 'data': rocks[6]},
    {'coords': (10,16), 'data': rocks[6]},

    {'coords': (11,15), 'data': rocks[7]},
    {'coords': (11,16), 'data': rocks[7]},

    {'coords': (12,15), 'data': rocks[8]},
    {'coords': (12,16), 'data': rocks[8]},
]



new_player = {
    "base": {
        "pid": '', 
        "name": '', 
        "password": '', 
        "rank": 1, 
        "title": "None", 
        "type": "None"
    },
    "stats": {
        "x": 2,
        "y": 2,
        "direction": "down",
        "total_time": 0
    },
    "client": {
        "x": 14,
        "y": 14
    },
    "skills": {
        "attack": {
            "level": 1,
            "xp": 0
        },
        "strength": {
            "level": 1,
            "xp": 0
        },
        "defence": {
            "level": 1,
            "xp": 0
        },
        "health": {
            "level": 5,
            "xp": 0
        },
        "magic": {
            "level": 1,
            "xp": 0
        },
        "ranged": {
            "level": 1,
            "xp": 0
        },
        "woodcutting": {
            "level": 1,
            "xp": 0
        },
        "mining": {
            "level": 1,
            "xp": 0
        },
        "firemaking": {
            "level": 1,
            "xp": 0
        }
    },
    "health": 25,
    "inventory": {
        "slots": [
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {}
        ],
        "equipped": {
            "head": {},
            "body": {},
            "gloves": {},
            "legs": {},
            "boots": {},
            "left_hand": {},
            "right_hand": {},
            "cape": {},
            "ring": {},
            "amulet": {},
            "arrow": {}
        }
    }
}

# tile_sample = {
#     'tile_id': str, # order of importance: object, entity, item
#     'tile': {
#         'object': {
#             'id': int, 
#             'name': str,
#             'description': str,
#             'tier': int, 
#             'health': int, 
#             'resource': str
#         },
#         'entity': {
#             'id': int,
#             'pid': int,
#             'name': str,
#             'type': str,
#             'health': int,
#             'combat_level': int
#         },
#         'item': {
#             'id': int,
#             'name': str,
#             'description': str,
#             'item_type': str,
#             'level': int,
#             'value': int,
#             'damage': int,
#             'defense': int,
#         },
#     }
# }

