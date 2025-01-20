from grid_server.classes.items.item import Item

class Armor(Item):
    def __init__(self, name, description, tier, slot, type):
        super().__init__(name, description, tier)
        self.slot = slot
        self.armor = tier * 10
        self.equippable = True
        self.type = type

    def equip(self, entity):
        entity.equip(self)

    def unequip(self, entity):
        entity.unequip(self)

    def to_dict(self):
        data = super().to_dict()
        data['slot'] = self.slot
        data['armor'] = self.armor
        data['type'] = self.type
        return data

    @staticmethod
    def create_armor(name, description, tier, slot, type):
        return Armor(name, description, tier, slot, type)
    

