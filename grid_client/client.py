import json
import socket
import struct
import threading
import numpy as np
import tty
import termios
import sys
import curses
import pickle
import base64

# COLOR = {
#     'WHITE': ' ',
#     'BLACK': '█',
#     'GREEN': 'G',
#     'BLUE': 'B',
#     'RED': 'R',
#     'YELLOW': 'Y',
#     'CYAN': 'C',
#     'MAGENTA': 'M',
#     'GRAY': '.',
# }

ID = {
    'tbu': f'֍֎۩۝۞ѺѺ҈҉⌂●○◌◊﴾﴿',
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

class GridWorldRenderer:
    def __init__(self):
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
        self.last_grid = None  # Add this line to store the previous grid state

    def hex_to_rgb(self, hex):
        # Define your hex color
        # hex_color = {
        #     1: '#FFFFFF', # White
        #     2: '#000000', # Black
        #     3: '#008000', # Green
        #     4: '#0000FF', # Blue
        #     5: '#FF0000', # Red
        #     6: '#FFFF00', # Yellow
        #     7: '#00FFFF', # Cyan
        #     8: '#FF00FF', # Magenta
        #     9: '#808080', # Gray
        #     10: '#FFA500', # Orange
        #     11: '#800080', # Purple
        #     12: '#00FF00', # Lime
        #     13: '#00FFFF', # Aqua
        #     14: '#FF00FF', # Fuchsia
        #     15: '#800000', # Maroon
        #     16: '#000080', # Navy
        #     17: '#808000', # Olive
        #     18: '#800000', # Purple
        #     19: '#008080', # Teal
        #     20: '#FF4500', # OrangeRed
        #     21: '#FF69B4', # HotPink
        #     22: '#FF6347', # Tomato
        #     23: '#FFD700', # Gold
        #     24: '#FFA07A', # LightSalmon
        #     26: '#FFC0CB', # Pink

        # } 

        # for k, v in hex_color.items():
        #     r, g, b = self.hex_to_rgb(v)
        #     curses.init_color(k, r, g, b)
        r, g, b = int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:7], 16)
        return int(r / 255 * 1000), int(g / 255 * 1000), int(b / 255 * 1000)

    def init_curses(self, stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

        self.init_colors()
        
        height, width = stdscr.getmaxyx()
        screen_width = width // 2
        qwidth = width // 4
        text_height = height // 2

        self.screen_panel = curses.newwin(height, screen_width, 0, 0)
        self.menu_right_panel = curses.newwin(text_height, qwidth, 0, screen_width + qwidth)
        self.menu_left_panel = curses.newwin(text_height, qwidth, 0, screen_width)
        self.text_panel = curses.newwin(text_height, screen_width, text_height, screen_width)

    def tile_examine(self):
        if self.player['direction'] == 'up':
            tile = self.grid_world[self.player['local_coords']['x'] - 1][self.player['local_coords']['y']]
        elif self.player['direction'] == 'down':
            tile = self.grid_world[self.player['local_coords']['x'] + 1][self.player['local_coords']['y']]
        elif self.player['direction'] == 'left':
            tile = self.grid_world[self.player['local_coords']['x']][self.player['local_coords']['y'] - 1]
        elif self.player['direction'] == 'right':
            tile = self.grid_world[self.player['local_coords']['x']][self.player['local_coords']['y'] + 1]
        return tile
    
    def tile_pan(self):
        tile = self.tile_examine()
        line = 1
        if tile.object is not None:
            object = tile.object
            self.menu_right_panel.addstr(line, 1, f"{object['name']}:")
            line += 1
            self.menu_right_panel.addstr(line, 1, f"  Tier: {object['tier']}")
            line += 1
            self.menu_right_panel.addstr(line, 1, f"  Health: {object['health']}")
            line += 1
            self.menu_right_panel.addstr(line, 1, f"  Resource: {object['resource']}")
            line += 1
        if tile.entity is not None:
            entity = tile.entity
            self.menu_right_panel.addstr(line, 1, f"{entity['name']}:")
            line += 1
            self.menu_right_panel.addstr(line, 1, f"  Combat Level: {entity['combat_level']}")
            line += 1
            self.menu_right_panel.addstr(line, 1, f"  Health: {entity['health']}")
            line += 1
            self.menu_right_panel.addstr(line, 1, f"  Type: {entity['type']}")
            line += 1
        if tile.item is not None:
            item = tile.item
            self.menu_right_panel.addstr(line, 1, f"{item['name']}:")
            line += 1
            self.menu_right_panel.addstr(line, 1, f"  Value: {item['value']}")
            line += 1
            self.menu_right_panel.addstr(line, 1, f"  Level: {item['level']}")
            line += 1

    def unpack_data(self, data):
        player_data = data['player']
        self.player = {
            'id': player_data['id'],
            'pid': player_data['pid'],
            'name': player_data['name'],
            'type': player_data['type'],
            'coords': player_data['coords'],
            'local_coords': player_data['local_coords'],
            'direction': player_data['direction'],
            'skills': player_data['skills'],
            'xp': player_data['xp'],
            'max_health': player_data['max_health'],
            'health': player_data['health'],
            'inventory': player_data['inventory'],
            'combat_level': player_data['combat_level']
        }
        # Decode and deserialize the base64-encoded array
        self.grid_world = pickle.loads(base64.b64decode(data['array']))
        self.grid_shape = self.grid_world.shape
        self.text = data['text']

    def update(self, data):
        self.unpack_data(data)
        self.call_panels()
        self.update_panels()
        self.refresh_panels()

    def check_tile(self, x, y):
        tile = self.grid_world[x][y]
        # print(tile)
        if tile.object is not None:
            tile.id = tile.object['id']
        elif tile.entity is not None:
            tile.id = tile.entity['id']
        elif tile.item is not None:
            tile.id = tile.item['id']
        return tile
    
    def create_tile(self, x, y):
        tile = self.check_tile(x, y)
        if y == self.player['local_coords']['y'] and x == self.player['local_coords']['x']:
            cell, color = self.create_player_tile(self.player)
            self.screen_panel.addstr(x, y * 2, cell, curses.color_pair(color))
        else:
            cell = ID[tile.id]
            color = self.get_color(tile)
            try:
                self.screen_panel.addstr(x, y * 2, cell, curses.color_pair(color))
            except:
                pass
        return cell, color
    
    def create_player_tile(self, player):
        cell = ID[player['direction']]
        color = self.fg['cyan'] + self.bg['black']
        return cell, color

    def get_color(self, tile):
        fg = self.fg['white']
        bg = self.bg['black']

        if tile.id != 0:
            if tile.object is not None:
                object = tile.object
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
                if tile.id == 3:
                    if entity['combat_level'] > self.player['combat_level']:
                        fg = self.fg['red']
                    elif entity['combat_level'] == self.player['combat_level']:
                        fg = self.fg['yellow']
                    elif entity['combat_level'] < self.player['combat_level']:
                        fg = self.fg['green']

            # if tile.item is not None:
            #     bg = self.bg['magenta']

        return fg + bg

    def draw_screen(self):
        if self.last_grid is None:
            self.last_grid = np.zeros_like(self.grid_world)
        
        for x in range(self.grid_shape[0]):
            for y in range(self.grid_shape[1]):
                if self.grid_world[x][y] != self.last_grid[x][y]:
                    self.create_tile(x, y)
        
        self.last_grid = np.copy(self.grid_world)

    def call_panels(self):
        self.screen_panel.clear()
        self.text_panel.clear()
        self.menu_right_panel.clear()
        self.menu_left_panel.clear()
        self.text_panel.box()
        self.menu_right_panel.box()
        self.menu_left_panel.box()

    def refresh_panels(self):
        self.screen_panel.refresh()
        self.text_panel.refresh()
        self.menu_right_panel.refresh()
        self.menu_left_panel.refresh()
    
    def update_panels(self):
        self.player_pan()
        self.tile_pan()
        self.draw_screen()

    def player_pan(self):
        self.menu_left_panel.addstr(1, 1, f"Player: {self.player['name']}")
        self.menu_left_panel.addstr(2, 1, f"Health: {self.player['health']}/{self.player['max_health']}")
        self.menu_left_panel.addstr(3, 1, f"Combat Level: {self.player['combat_level']}")
        self.menu_left_panel.addstr(4, 1, f"Coords: ({self.player['coords']['x']}, {self.player['coords']['y']})")

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


class Client:
    def __init__(self, config):
        self.config = config
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((config["host"], int(config["port"])))
        self.render = GridWorldRenderer()
        self.button_handler = ButtonHandler()
        self.response = None
        self.username = None
        self.password = None
   
    def create_packet(self, type, data):
        packet = {
            'type': type if type is not None else 'none',
            'data': data if data is not None else {}
        }
        packet = json.dumps(packet).encode('utf-8')
        length = len(packet).to_bytes(4, byteorder='big')
        return length + packet

    def unpack_packet(self, header):
        data_length = int.from_bytes(header, byteorder='big')
        data = b''
        while len(data) < data_length:
            packet = self.client.recv(data_length - len(data))
            if not packet:
                break
            data += packet
        return data

    def receive_data(self):
        self.render.call_panels()
        while True:
            try:
                header = self.client.recv(4)
                if not header:
                    break
                data = self.unpack_packet(header)
                req = json.loads(data.decode('utf-8'))


                if req['type'] == 'game_state':
                    self.render.update(req['data'])


            except (ConnectionResetError, struct.error) as e:
                print(str(e))
                break

    def handle_input(self, stdscr):
        stdscr.nodelay(True)
        stdscr.timeout(100)  # Add this line to set a timeout for getch
        while True:
            command = stdscr.getch()
            if command == -1:
                continue
            action = self.button_handler.handle_button_press(chr(command))
            if chr(command) == 'q':
                packet = self.create_packet('move', {'move': action})
                self.client.sendall(packet)
                self.close()
                break
            if action is not None:
                packet = self.create_packet('move', {'move': action})
                self.client.sendall(packet)
            if chr(command) == 'e':
                if self.render.flag:
                    self.render.flag = False
                else:
                    self.render.flag = True

    def login(self):
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")
        packet = self.create_packet('login', {'username': self.username, 'password': self.password})
        self.client.send(packet)

    def main(self):
        self.login()
        curses.wrapper(self.curses_main)

    def curses_main(self, stdscr):
        self.render.init_curses(stdscr)
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()
        self.handle_input(stdscr)

    def close(self):
        curses.endwin()
        self.client.close()

class ButtonHandler:
    def __init__(self):
        self.up = 'w'
        self.left = 'a'
        self.down = 's'
        self.right = 'd'
        self.print = 'p'
        self.quit = 'q'
        self.attack = 'f'
        self.panel_flag = 'e'

    def handle_button_press(self, command):
        if command == self.quit:
            return 'quit'
        elif command == self.up:
            action = 'up'
        elif command == self.left:
            action = 'left'
        elif command == self.down:
            action = 'down'
        elif command == self.right:
            action = 'right'
        elif command == self.print:
            action = 'print'
        elif command == self.attack:
            action = 'interact'
        elif command == self.panel_flag:
            action = None

        else:
            action = None
        return action
    
if __name__ == "__main__":
    Client().main()
