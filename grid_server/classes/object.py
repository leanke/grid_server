from grid_server.classes.array import GameArray
from grid_server.classes.data import obj_ids, objects

class GameObject:
    def __init__(self, coords, obj_id, drop_table=None, status=None):
        self.objects = []
        self.coords = coords
        self.obj_id = obj_id
        self.drop_table = drop_table
        self.status = status
        # for obj_list in data.values():
        #     for obj in obj_list:
        #         self.objects.append({
        #             'x': obj['x'],
        #             'y': obj['y'],
        #             'id': obj['type'],
        #             'type': obj['type'],
        #             'status': None
        #         })

    def action(self, obj_id):
        for obj in self.objects:
            if obj['id'] == obj_id:
                obj['status'] = 'depleted'
                break

    def place(self):
        pass
