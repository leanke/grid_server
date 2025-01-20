from grid_server.classes.items.item import Item

class Resource(Item):
    def __init__(self, name, description, level, stackable=False, quantity=1):
        super().__init__(name, description, level, stackable, quantity)

    @staticmethod
    def create_resource(name, description, level, stackable=False, quantity=1):
        return Resource(name, description, level, stackable, quantity)
    
    def to_dict(self):
        data = super().to_dict()
        return data

