class NPC:
    def __init__(self, ent_id, pid, name, combat_level, health, type):
        self.ent_id = ent_id
        self.pid = pid
        self.name = name
        self.type = type
        self.combat_level = combat_level
        self.health = health


    @staticmethod
    def create_npc(ent_id, pid, name, type, combat_level, health):
        return NPC(ent_id, pid, name, type, combat_level, health)
