import json
import os
import pdb
import random
import numpy as np
import curses
from grid_server.classes.data import objects, items
from grid_server.classes.entities.player import Player
from grid_server.classes.environment import GridWorld
from grid_server.classes.entities.npc import Mage, Warrior, Archer
from grid_server.classes.entities.entity import Entity


ID = {
    'tbu': f'֍֎۩۝۞ѺѺ҈҉⌂●○◌◊﴾﴿',
    'tbu10': '▁▂▃▄▅▆▇█▉▊▋▌▍▎▏',
    'tbu11': '▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟',
    'tbu12': '□▢▣▤▥▦▧▨▩▪▫▬▭▮▯',
    'tbu13': '▰▱▲△▴▵▶▷▸▹►▻▼▽▾▿',
    'tbu14': '◀◁◂◃◄◅◆◇◈◉◊○◌◍◎',
    'tbu15': '●◐◑◒◓◔◕◖◗◘◙◚◛◜◝◞◟',
    'tbu16': '◠◡◢◣◤◥◦◧◨◩◪◫◬◭◮◯',
    'tbu17': '◰◱◲◳◴◵◶◷◸◹◺◻◼◽◾◿',
    'tbu18': '─│┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬',
    'tbu19': 'ꟀꝊₒ⁰ꟁꝋṍṏṑṓᶿᶲᶱᵟᵒᴼᵓᵔᵕᵖᵗᵘᵙᵚᵛᵜᵝᵞᵟᵠᵡᵢᵣᵤᵥᵦᵧᵨᵩᵪᵫᵬᵭᵮᵯᵰᵱᵲᵳᵴᵵᵶᵷᵸᵹᵺᵻᵼᵽᵾᵿ',
    'new': '       ■  ▀     ',
    "up": '▲',
    "down": '▼',
    "left": '◄',
    "right": '►',
    0: '.',
    1: 'T',
    2: 'R',
    3: 'P',
    4: '█',
    5: '?',
    20: 'T'
}
PLR = {
    'up': '▲',
    'down': '▼',
    'left': '◄',
    'right': '►'
}

ENT = {
    1: 'ꟁ',
    2: 'ṏ',
    3: 'ꝋ',
    4: 'ṍ',
    5: 'ṑ',
    6: 'ṓ',
}
ITM = {
#     1: 'ᴼ',
#     2: 'ᶿ',
#     3: 'ᶲ',
#     4: 'ᶱ',
#     5: 'ᵟ',
#     6: 'ᵒ',
#     7: 'ᵡ',
#     8: 'ᵓ',
#     9: 'ᵔ',
#     10: 'ᵕ',
#     11: 'ᵖ',
#     12: 'ᵗ',
#     13: 'ᵘ',
#     14: 'ᵙ',
#     15: 'ᵚ',
#     16: 'ᵛ',
#     17: 'ᵜ',
#     18: 'ᵝ',
#     19: 'ᵞ',
#     20: 'ᵟ',
#     21: 'ᵠ',
# }
    1: '◊',
    2: '◌',
    3: '○',
    4: '●',
    5: '⌂',
    6: '҈',
    7: '҉',
    8: 'Ѻ',
    9: 'Ѻ',
    10: '۩',
    11: '۝',
    12: '۞',
    13: '֍',
    14: '֎',
}
WALL = {
    1: '☰',
    2: '☱',
    3: '☲',
    4: '☳',
    5: '☴',
    6: '☵',
    7: '☶',
    8: '☷',
}
OBJ = {
    1: 'T',
    2: 'R',
    3: 'P',
    4: WALL[1],
}

class EditorRenderer:
    def __init__(self, player, grid_world):
        self.text_queue = []
        self.flag = False
        self.tile = {}
        self.fg = {
            'white': 1,
            'black': 2,
            'green': 3,
            'blue': 4,
            'red': 5,
            'yellow': 6,
            'cyan': 7,
            'magenta': 8,
        }
        self.bg = {
            'white': 10,
            'black': 20,
            'green': 30,
            'blue': 40,
            'red': 50,
            'yellow': 60,
            'cyan': 70,
            'magenta': 80,
        }
        self.last_grid = None  
        self.player = player
        self.grid_world = grid_world
        self.clear_line = ' ' * 25
        self.tile_pan_lines = 0
        self.player_pan_lines = 0
        self.text_pan_lines = 0

    def init_curses(self, stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        self.stdscr = stdscr

        self.init_colors()
        
        height, width = stdscr.getmaxyx()
        screen_width = width // 2
        qwidth = width // 4
        text_height = height // 2

        self.screen_panel = curses.newwin(height, screen_width, 0, 0)
        self.menu_right_panel = curses.newwin(text_height, qwidth, 0, screen_width + qwidth)
        self.menu_left_panel = curses.newwin(text_height, qwidth, 0, screen_width)
        self.text_panel = curses.newwin(text_height, screen_width, text_height, screen_width)
        # self.update(self.grid_world.grid.client_view(self.player))

    def tile_pan(self):
        for i in range(self.tile_pan_lines):
            self.menu_right_panel.addstr(i+1, 1, self.clear_line)
        self.menu_right_panel.refresh()
        line = 1
        tiles_coords = self.player.get_area_of_tiles(3)
        # self.text_panel.addstr(5, 1, f"({tiles_coords})")
        dropped_items = []
        for coords in tiles_coords:
            x, y = coords
            tile = self.grid_world.grid.get_tile(x, y)
            # if x != self.player.x and y != self.player.y:
            if tile.object is not None:
                object = tile.object
                self.menu_right_panel.addstr(line, 1, f"{object['name']}:")
                line += 1
                self.menu_right_panel.addstr(line, 1, f"  Tier: {object['tier']}")
                line += 1
            if tile.entity is not None:
                entity = tile.entity
                if tile.entity['pid'] != self.player.pid:
                    self.menu_right_panel.addstr(line, 1, f"{entity['name']}:")
                    line += 1
                    self.menu_right_panel.addstr(line, 1, f"  Combat Level: {entity['combat_level']}")
                    line += 1
                    self.menu_right_panel.addstr(line, 1, f"  Health: {entity['health']}")
                    line += 1
            if tile.items is not None and tile.items != []:
                item = tile.items
                for i in item:
                    dropped_items.append(i['name'])
        if dropped_items != []:
            self.menu_right_panel.addstr(line, 1, f"Dropped Items:")
            line += 1
            for i in dropped_items:
                self.menu_right_panel.addstr(line, 1, f"  {i}")
                line += 1

        self.tile_pan_lines = line

    def update(self, data):
        _ , client_view = data
        self.call_panels()
        self.update_panels(client_view)
        self.refresh_panels()
    
    def create_tile(self, tile):
        # print(tile.entity)
        if tile.id == 'object':
            if tile.object['id'] == 4:
                id = WALL[tile.object['tier']]
            id = OBJ[tile.object['id']]
        elif tile.id == 'entity':
            id = ENT[tile.entity['id']]
        else:
            id = '.'
        
        if tile.entity is not None and tile.entity['pid'] == self.player.pid:
            cell, color = self.create_player_tile(self.player, tile)
        else:
            cell = id
            color = self.get_color(tile)
        return cell, color
    
    def create_player_tile(self, player, tile):
        cell = PLR[player.direction]
        bg = self.bg['black']
        if tile.items != [] and tile.items is not None:
            bg = self.bg['magenta']
        color = self.fg['cyan'] + bg
        return cell, color

    def get_color(self, tile):
        fg = self.fg['white']
        bg = self.bg['black']

        if tile.id != None:
            if tile.object is not None:
                object = tile.object
                if object['id'] != 4:
                    if object['tier'] == 1:
                        fg = self.fg['white']
                    elif object['tier'] == 2:
                        fg = self.fg['green']
                    elif object['tier'] == 3:
                        fg = self.fg['yellow']
                    elif object['tier'] == 4:
                        fg = self.fg['red']
                    elif object['tier'] == 5:
                        fg = self.fg['cyan']
                    elif object['tier'] == 6:
                        fg = self.fg['magenta']
                    else:
                        fg = self.fg['white']
            

            if tile.entity is not None:
                entity = tile.entity
                if tile.id == 'entity':
                    if entity['combat_level'] > self.player.combat_level:
                        fg = self.fg['red']
                    elif entity['combat_level'] == self.player.combat_level:
                        fg = self.fg['yellow']
                    elif entity['combat_level'] < self.player.combat_level:
                        fg = self.fg['green']

            if tile.items != [] and tile.items is not None:
                bg = self.bg['magenta']
                if tile.object is None and tile.entity is None:
                        fg = self.fg['black']

        return fg + bg

    def draw_screen(self, grid):
        if grid is not None:
            for x in range(grid.shape[0]):
                for y in range(grid.shape[1]):
                    new_tile = grid[x][y]
                    if self.last_grid is not None:
                        old_tile = self.last_grid[x][y]
                        if new_tile != old_tile:
                            tile, color = self.create_tile(new_tile)
                            # self.screen_panel.addstr(x, y * 2, tile, curses.color_pair(color))
                            self.screen_panel.addch(x, y * 2, tile, curses.color_pair(color))
                            self.screen_panel.refresh()
                    else:
                        tile, color = self.create_tile(new_tile)
                        # self.screen_panel.addstr(x, y * 2, tile, curses.color_pair(color))
                        self.screen_panel.addch(x, y * 2, tile, curses.color_pair(color))
                        self.screen_panel.refresh()
            self.last_grid = grid

    def call_panels(self):
        # # self.screen_panel.clear()
        # self.text_panel.clear()
        # self.menu_right_panel.clear()
        # self.menu_left_panel.clear()
        self.text_panel.box()
        self.menu_right_panel.box()
        self.menu_left_panel.box()

    def refresh_panels(self):
        self.screen_panel.refresh()
        for i, text in enumerate(self.text_queue):
            self.text_panel.addstr(i + 1, 1, text)
        self.text_panel.refresh()
        self.menu_right_panel.refresh()
        self.menu_left_panel.refresh()
    
    def update_panels(self,client_view):
        self.player_pan()
        self.tile_pan()
        # self.text_pan()
        self.draw_screen(client_view)

    def player_pan(self):
        for i in range(self.player_pan_lines):
            self.menu_left_panel.addstr(i+1, 1, self.clear_line)
        self.menu_left_panel.refresh()
        line = 1
        self.menu_left_panel.addstr(1, 1, f"Player: {self.player.name}")
        line += 1
        self.menu_left_panel.addstr(2, 1, f"Health: {self.player.health}/{self.player.max_health}")
        line += 1
        self.menu_left_panel.addstr(2, 1, f"Combat Level: {self.player.combat_level}")
        line += 1
        self.menu_left_panel.addstr(3, 1, f"Coords: ({self.player.x}, {self.player.y})")
        line += 1
        self.player_pan_lines = line

    def obj(self, obj, tier):
        obj = objects[obj][tier]
        return obj
    
    def ent(self, ent, coords):
        if ent == 1:
            ent = Entity(coords, 1, 'Entity', 0).__dict__
        elif ent == 2:
            ent = Mage(coords, 2, 'Mage', 0).__dict__
        elif ent == 3:
            ent = Warrior(coords, 3, 'Warrior', 0).__dict__
        elif ent == 4:
            ent = Archer(coords, 4, 'Archer', 0).__dict__
        else:
            ent = None
        return ent
    
    def itm(self, itm, tier):
        itm = items[itm][tier]
        return itm

    def text_pan(self, tile, type, coords=None):
        x, y = self.player.get_target_tile()
        for i in range(self.text_pan_lines):
            self.text_panel.addstr(i+1, 1, self.clear_line)
        self.text_panel.refresh()
        line = 1
        self.text_panel.addstr(1, 1, f"Editing tile at ({x}, {y})")
        line += 1
        self.text_panel.addstr(2, 1, f"Creating {type}")
        line += 1
        self.text_panel.addstr(3, 1, "Enter ID: ")
        line += 1
        self.text_panel.refresh()
        id = int(self.text_panel.getstr().decode('utf-8'))
        # self.text_panel.refresh()
        if type == 'object':
            self.text_panel.addstr(4, 1, "Enter object tier: ")
            line += 1
            self.text_panel.refresh()
            tier = int(self.text_panel.getstr().decode('utf-8'))
            data = self.obj(id, tier)

        elif type == 'entity':
            data = self.ent(id, coords)

        elif type == 'item':
            self.text_panel.addstr(4, 1, "Enter item tier: ")
            line += 1
            self.text_panel.refresh()
            tier = int(self.text_panel.getstr().decode('utf-8'))
            data = self.itm(id, tier)
        else:
            data = None
            type = None
        if type is not None:
            tile.set(type, data)
            if len(self.text_queue) > 10:
                self.text_queue.pop(0)
            self.text_queue.append(f"added {data['name']} to tile")
            line += 1
        self.update(self.grid_world.grid.client_view(self.player))
        self.text_pan_lines = line

    def init_colors(self):
        curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(13, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(14, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(15, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(16, curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(17, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(18, curses.COLOR_MAGENTA, curses.COLOR_WHITE)

        curses.init_pair(21, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(22, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(23, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(24, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(25, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(26, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(27, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(28, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        curses.init_pair(31, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(32, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(33, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(34, curses.COLOR_BLUE, curses.COLOR_GREEN)
        curses.init_pair(35, curses.COLOR_RED, curses.COLOR_GREEN)
        curses.init_pair(36, curses.COLOR_YELLOW, curses.COLOR_GREEN)
        curses.init_pair(37, curses.COLOR_CYAN, curses.COLOR_GREEN)
        curses.init_pair(38, curses.COLOR_MAGENTA, curses.COLOR_GREEN)

        curses.init_pair(41, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(42, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(43, curses.COLOR_GREEN, curses.COLOR_BLUE)
        curses.init_pair(44, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(45, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(46, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.init_pair(47, curses.COLOR_CYAN, curses.COLOR_BLUE)
        curses.init_pair(48, curses.COLOR_MAGENTA, curses.COLOR_BLUE)

        curses.init_pair(51, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(52, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(53, curses.COLOR_GREEN, curses.COLOR_RED)
        curses.init_pair(54, curses.COLOR_BLUE, curses.COLOR_RED)
        curses.init_pair(55, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(56, curses.COLOR_YELLOW, curses.COLOR_RED)
        curses.init_pair(57, curses.COLOR_CYAN, curses.COLOR_RED)
        curses.init_pair(58, curses.COLOR_MAGENTA, curses.COLOR_RED)

        curses.init_pair(61, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(62, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(63, curses.COLOR_GREEN, curses.COLOR_YELLOW)
        curses.init_pair(64, curses.COLOR_BLUE, curses.COLOR_YELLOW)
        curses.init_pair(65, curses.COLOR_RED, curses.COLOR_YELLOW)
        curses.init_pair(66, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        curses.init_pair(67, curses.COLOR_CYAN, curses.COLOR_YELLOW)
        curses.init_pair(68, curses.COLOR_MAGENTA, curses.COLOR_YELLOW)

        curses.init_pair(71, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(72, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(73, curses.COLOR_GREEN, curses.COLOR_CYAN)
        curses.init_pair(74, curses.COLOR_BLUE, curses.COLOR_CYAN)
        curses.init_pair(75, curses.COLOR_RED, curses.COLOR_CYAN)
        curses.init_pair(76, curses.COLOR_YELLOW, curses.COLOR_CYAN)
        curses.init_pair(77, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(78, curses.COLOR_MAGENTA, curses.COLOR_CYAN)

        curses.init_pair(81, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        curses.init_pair(82, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(83, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
        curses.init_pair(84, curses.COLOR_BLUE, curses.COLOR_MAGENTA)
        curses.init_pair(85, curses.COLOR_RED, curses.COLOR_MAGENTA)
        curses.init_pair(86, curses.COLOR_YELLOW, curses.COLOR_MAGENTA)
        curses.init_pair(87, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
        curses.init_pair(88, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)

    def close(self):
        curses.endwin()


class WorldEditor:
    def __init__(self):
        self.stdscr = None
        self.path = f'./grid_server/worlds/world_builder'
        self.player = None
        if not os.path.exists(self.path):
            self.create_world_files()
        self.grid_world = GridWorld(self.path)

    def create_world_files(self):
        """
        Create necessary files and directories for a new world.
        """
        userpath = self.path + '/users/'
        logpath = self.path + '/logs/'
        os.makedirs(self.path)
        os.makedirs(userpath)
        os.makedirs(logpath)
    
    def get_or_create_player(self, username, password):
        """
        Get an existing player or create a new one.
        """
        path = f'{self.path}/users/{username}'
        if not os.path.exists(f'{path}.json'):
            self.create_player(username, password, path)
        else:
            with open(f'{path}.json') as f:
                config = json.load(f)
                self.player = Player(config, path)
        if password != self.player.password:
            print("Invalid password")
    
    def create_player(self, username, password, path):
        """
        Create a new player.
        """
        os.system(f"touch {path}.json")
        os.system(f"cp ./grid_server/default.json {path}.json")
        _, _, files = next(os.walk(f'{self.path}/users/'))
        file_count = len(files)
        with open(f'{path}.json') as f:
            config = json.load(f)
            self.player = Player(config, path)
        self.player.name = username
        self.player.password = password
        self.player.pid = 1_000_000 + file_count
        self.player.save()

    def run(self):
        self.login()
        self.renderer = EditorRenderer(self.player, self.grid_world)
        curses.wrapper(self.curses_main)

    def curses_main(self, stdscr):
        self.renderer.init_curses(stdscr)
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        while True:
            x, y = self.player.get_target_tile()
            tile = self.grid_world.grid.get_tile(x, y)
            command = self.stdscr.getch()
            if command == ord('w') or command == ord('a') or command == ord('s') or command == ord('d'):
                self.handle_movement(command)
                self.renderer.update(self.grid_world.grid.client_view(self.player))
            if command == ord('q'):
                self.grid_world.grid.remove(self.player.x, self.player.y, 'entity')
                self.exit_editor()
            elif command == ord('1'):
                self.renderer.text_pan(tile, 'object')
            elif command == ord('2'):
                self.renderer.text_pan(tile, 'entity', coords=(x,y))
            elif command == ord('3'):
                self.renderer.text_pan(tile, 'item')
            elif command == ord('0'):
                tile.clear()
                self.renderer.update(self.grid_world.grid.client_view(self.player))
            elif command == ord('k'):
                self.save_world()
            elif command == ord('l'):
                self.load_world()

            # self.stdscr.refresh()

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        self.get_or_create_player(username, password)

    def handle_movement(self, command):
        if command == ord('w'):
            self.grid_world.step(self.player, 'up')
        elif command == ord('a'):
            self.grid_world.step(self.player, 'left')
        elif command == ord('s'):
            self.grid_world.step(self.player, 'down')
        elif command == ord('d'):
            self.grid_world.step(self.player, 'right')

    def save_world(self):
        self.stdscr.addstr(3, 0, "Enter filename to save: ")
        self.stdscr.refresh()
        filename = self.stdscr.getstr().decode('utf-8')
        self.grid_world.grid.save_to_file(filename)
        self.stdscr.addstr(4, 0, f"World saved to {filename}")
        self.stdscr.refresh()

    def load_world(self):
        self.stdscr.addstr(3, 0, "Enter filename to load: ")
        self.stdscr.refresh()
        filename = self.stdscr.getstr().decode('utf-8')
        self.grid_world.grid.world = self.grid_world.grid.load_from_file(filename)
        self.stdscr.addstr(4, 0, f"World loaded from {filename}")
        self.stdscr.refresh()

    def exit_editor(self):
        curses.endwin()
        exit()

if __name__ == "__main__":
    editor = WorldEditor()
    editor.run()
