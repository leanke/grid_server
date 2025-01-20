class Item:
    def __init__(self, name, description, level, stackable=False, quantity=1):
        self.name = name
        self.description = description
        self.level = level
        self.stackable = stackable
        self.quantity = quantity

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'level': self.level,
            'stackable': self.stackable,
            'quantity': self.quantity
        }