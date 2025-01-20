class Tile:
    def __init__(self, object=None, entity=None, items=None):
        self.object = object
        self.entity = entity
        self.items = items if items is not None else []
        self.id = None
        
    def get_id(self):
        if self.object is not None:
            return 'object'
        elif self.entity is not None:
            return 'entity'
        elif self.items != [] and self.items is not None:
            return 'item'
        else:
            return None

    def set(self, component_type, component):
        if component_type == 'object':
            if self.object is None:
                self.object = component
                self.id = component_type
        elif component_type == 'entity':
            if self.entity is None:
                self.entity = component
                if self.object is None:
                    self.id = component_type
                else:
                    self.id = 'object'       
        elif component_type == 'item':
            self.items.append(component)
            if self.object is None:
                if self.entity is None:
                    self.id = component_type
                else:
                    self.id = 'entity'
            else:
                self.id = 'object'
    
    def remove(self, component_type, component=None):
        if component_type == 'object':
            self.object = None
        elif component_type == 'entity':
            self.entity = None
        elif component_type == 'item':
            if component:
                self.items.remove(component)
            else:
                self.items.clear()
        else:
            raise ValueError("Invalid component type")
        self.id = self.get_id()

    def get(self, component_type):
        if component_type == 'object':
            return self.object
        elif component_type == 'entity':
            return self.entity
        elif component_type == 'item':
            return self.items
        else:
            raise ValueError("Invalid component type")

    def clear(self):
        self.object = None
        self.entity = None
        self.items = []
        self.id = 0



