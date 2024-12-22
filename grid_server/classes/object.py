from grid_server.classes.array import GameArray
from grid_server.classes.data import obj_ids, objects

class GameObject:
    def __init__(self, data):
        self.objects = []
        for obj_list in data.values():
            for obj in obj_list:
                self.objects.append({
                    'x': obj['x'],
                    'y': obj['y'],
                    'id': obj['type'],
                    'type': obj['type'],
                    'status': None
                })

    def action(self, obj_id):
        for obj in self.objects:
            if obj['id'] == obj_id:
                obj['status'] = 'depleted'
                break

    def place(self):
        pass
