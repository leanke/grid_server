class Tile:
    def __init__(self, object=None, entity=None, item=None):
        self.object = object
        self.entity = entity
        self.item = item
        self.id = self.get_id()

    def get_id(self):
        if self.object is not None:
            return self.object['id']
        elif self.entity is not None:
            return self.entity['id']
        elif self.item is not None:
            return self.item['id']
        else:
            return 0

    def set_object(self, obj):
        if self.object is None and self.entity is None:
            self.object = obj
            self.id = obj['id']
        else:
            raise ValueError("Tile already occupied by an object or entity")

    def set_entity(self, entity):
        if self.object is None and self.entity is None:
            self.entity = entity
            self.id = entity['id']
        elif self.object is None:
            self.entity = entity
            self.id = entity['id']
        else:
            raise ValueError("Tile already occupied by an object")

    def set_item(self, item):
        if self.object is None and self.item is None:
            self.item = item
            self.id = item['id']
        elif self.object is None:
            self.item = item
            self.id = item['id']
        else:
            raise ValueError("Tile already occupied by an object")

    def clear(self):
        self.object = None
        self.entity = None
        self.item = None
        self.id = 0
