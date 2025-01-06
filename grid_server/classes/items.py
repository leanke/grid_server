class Item:
    def __init__(self, item_id, name, description, level):
        self.id = item_id
        self.name = name
        self.description = description
        self.level = level
    
    @staticmethod
    def create_sword(level):
        return Item(1, 'Sword', 'A Sword', level)
    
    @staticmethod
    def create_shield(level):
        return Item(2, 'Shield', 'A Shield', level)
    
    @staticmethod
    def create_staff(level):
        return Item(3, 'Staff', 'A Staff', level)
    
    @staticmethod
    def create_bow(level):
        return Item(4, 'Bow', 'A Bow', level)

    @staticmethod
    def create_item(item_id, name, description, level):
        return Item(item_id, name, description, level)
