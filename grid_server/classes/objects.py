class GameObject:
    def __init__(self, id, name, description, tier, health, resource):
        self.id = id
        self.name = name
        self.description = description
        self.tier = tier
        self.health = health
        self.resource = resource

    @staticmethod
    def create_tree(tier, health, resource):
        return GameObject(1, 'Tree', 'A tree', tier, health, resource)

    @staticmethod
    def create_rock(tier, health, resource):
        return GameObject(2, 'Rock', 'A rock', tier, health, resource)
    
    @staticmethod
    def create_wall(tier, health, resource):
        return GameObject(4, 'Wall', 'A wall', tier, health, resource)
    
    @staticmethod
    def create_object(id, name, description, tier, health, resource):
        return GameObject(id, name, description, tier, health, resource)
