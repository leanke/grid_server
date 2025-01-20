from grid_server.classes.items.item import Item

class Weapon(Item):
    def __init__(self, name, description, tier, slot, type):
        super().__init__(name, description, tier)
        self.slot = slot
        self.damage = tier * 10
        self.equippable = True
        self.type = type

    def equip(self, entity):
        entity.equip(self)

    def unequip(self, entity):
        entity.unequip(self)

    def to_dict(self):
        data = super().to_dict()
        data['slot'] = self.slot
        data['damage'] = self.damage
        data['type'] = self.type
        return data

    @staticmethod
    def create_weapon(name, description, tier, slot, type):
        return Weapon(name, description, tier, slot, type)
