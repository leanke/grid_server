import configparser

class Player:
    def __init__(self, ini_file):
        self.config = configparser.ConfigParser()
        self.ini_file = ini_file
        self.load()

    def load(self):
        self.config.read(self.ini_file)
        # print(self.config.read(self.ini_file))
        self.name = self.config.get('base', 'name')
        self.rank = self.config.get('base', 'rank')
        self.title = self.config.get('base', 'title')
        self.type = self.config.get('base', 'type')
        self.x = self.config.getint('stats', 'x')
        self.y = self.config.getint('stats', 'y')
        self.total_time = self.config.getint('stats', 'total_time')
        self.skills = {
            'attack': self.config.getint('skills', 'attack'),
            'defence': self.config.getint('skills', 'defence'),
            'health': self.config.getint('skills', 'health'),
            'woodcutting': self.config.getint('skills', 'woodcutting'),
            'mining': self.config.getint('skills', 'mining'),
        }

    def save(self, base, name, value):
        self.config.set(base, name, str(value))
        with open(self.ini_file, 'w') as configfile:
            self.config.write(configfile)

    def info(self):
        string = (
            f"Info:\n" +
            f"  Username: {self.config.get('base', 'name')}\n" + 
            f"  Rank: {self.config.get('base', 'rank')}\n" +
            f"  Title: {self.config.get('base', 'title')}\n" +
            f"  Coords: ({self.config.getint('stats', 'x')}, {self.config.getint('stats', 'y')})\n" +
            f"  Skills:\n"
            f"    Attack: {self.config.getint('skills', 'attack')}, Defence: {self.config.getint('skills', 'defence')}, Health: {self.config.getint('skills', 'health')}\n" +
            f"    Woodcutting: {self.config.getint('skills', 'woodcutting')}, Mining: {self.config.getint('skills', 'mining')}\n"
            )
        return string

# Example usage:
# player = Player('leanke.ini')
# player.name = "new_name"
# player.save_player_data()