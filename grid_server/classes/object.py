from grid_server.classes.array import GameArray
from grid_server.classes.data import obj_ids, objects

class GameObject:
    def __init__(self, obj_dict):
        self.object = obj_dict['obj_id']
        self.coords = obj_dict['coords']
        self.status = obj_dict['status']
        self.drop_table = obj_dict['drop_table']

    def action(self, obj_id):
        for obj in self.objects:
            if obj['id'] == obj_id:
                obj['status'] = 'depleted'
                break

    def place(self):
        pass
