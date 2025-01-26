from grid_server.classes.entities.entity import Entity
from grid_server.classes.items.item_data import items

class Mage(Entity):
    def __init__(self, coords, *args, **kwargs):
        super().__init__(coords, id=2, name='Mage', **kwargs)
        self.x, self.y = coords
        self.home = coords
        self.skills.set_level('magic', 5)
        self.skills.set_level('defence', 5)
        self.combat_level = self.skills.combat_level()
        equips = ['head', 'body', 'legs', 'hands', 'feet', 'right_hand']
        # for equip in equips:
        #     self.inventory.equip(items['magic_items'][equip]['novice'])

    # 'head': magic_hat,
    # 'body': magic_robe_top,
    # 'legs': magic_robe_bottom,
    # 'hands': magic_gloves,
    # 'feet': magic_boots,
    # 'right_hand': staffs,
    # 'left_hand': orb,


class Warrior(Entity):
    def __init__(self, coords, *args, **kwargs):
        super().__init__(coords, id=3, name='Warrior', **kwargs)
        self.x, self.y = coords
        self.home = coords
        self.skills.set_level('strength', 3)
        self.skills.set_level('defence', 5)
        self.skills.set_level('attack', 3)
        self.combat_level = self.skills.combat_level()

class Archer(Entity):
    def __init__(self, coords, *args, **kwargs):
        super().__init__(coords, id=4, name='Archer', **kwargs)
        self.x, self.y = coords
        self.home = coords
        self.skills.set_level('ranged', 5)
        self.skills.set_level('defence', 5)
        self.combat_level = self.skills.combat_level()




