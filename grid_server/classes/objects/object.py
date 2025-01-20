class TileObj:
    def __init__(self, id, name, description, tier, health, resource):
        self.id = id
        self.name = name
        self.description = description
        self.tier = tier
        self.health = health
        self.resource = resource
    
    @staticmethod
    def create_object(id, name, description, tier, health, resource):
        return TileObj(id, name, description, tier, health, resource)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'tier': self.tier,
            'health': self.health,
            'resource': self.resource
        }
