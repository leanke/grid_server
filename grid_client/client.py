import json
import random
import socket
import struct
import threading
import numpy as np
import curses
import curses.textpad
import pickle
import base64
import grid_client.client_data as data





class Renderer:
    def __init__(self):
        self.text_queue = []
        self.flag = False
        self.tile = {}
        self.last_grid = None  
        self.player = None
        self.grid_world = None
        self.tile_pan_lines = 0
        self.welcome_text = True

    def init_curses(self, stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        stdscr.keypad(1)
        self.stdscr = stdscr

        
        
        height, width = stdscr.getmaxyx()
        screen_width = width // 2
        qwidth = width // 4
        text_height = height // 2

        self.screen_panel = curses.newwin(height, screen_width, 0, 0)
        self.menu_right_panel = curses.newwin(text_height, qwidth, 0, screen_width + qwidth)
        self.menu_left_panel = curses.newwin(text_height, qwidth, 0, screen_width)
        self.text_panel = curses.newwin(text_height, screen_width, text_height, screen_width)

    def tile_pan(self):
        line = 1
        tiles_coords = self.get_area_of_tiles(1)
        dropped_items = []
        my, mx = self.text_panel.getmaxyx()
        for i in range(my - 2):
            self.menu_right_panel.addstr(i+1, 1, ' ' * (mx - 2))
        self.menu_right_panel.box()
        if not self.flag:
            for coords in tiles_coords:
                x, y = coords
                tile = self.grid_world[x][y]
                if line > my - 2:
                    break
                if tile.object is not None:
                    object = tile.object
                    self.menu_right_panel.addstr(line, 1, f"{object['name']}:" + (' ' * (x - 2 - len(f"{object['name']}:"))))
                    line += 1
                    self.menu_right_panel.addstr(line, 1, f"  Tier: {object['tier']}" + (' ' * (x - 2 - len(f"  Tier: {object['tier']}"))))
                    line += 1
                if tile.entity is not None:
                    entity = tile.entity
                    if tile.entity.pid != self.player['pid']:
                        self.menu_right_panel.addstr(line, 1, f"{entity.name}:" + (' ' * (x - 2 - len(f"{entity.name}:"))))
                        line += 1
                        self.menu_right_panel.addstr(line, 1, f"  Combat Level: {entity.combat_level}" + (' ' * (x - 2 - len(f"  Combat Level: {entity.combat_level}"))))
                        line += 1
                        self.menu_right_panel.addstr(line, 1, f"  Health: {entity.health}" + (' ' * (x - 2 - len(f"  Health: {entity.health}"))))
                        line += 1
                if tile.items is not None and tile.items != []:
                    item = tile.items
                    for i in item:
                        dropped_items.append(i['name'])
            if dropped_items != []:
                self.menu_right_panel.addstr(line, 1, f"Dropped Items:" + (' ' * (x - 2 - len(f"Dropped items:"))))
                line += 1
                for i in dropped_items:
                    self.menu_right_panel.addstr(line, 1, f"  {i}" + (' ' * (x - 2 - len(f"{i}"))))
                    line += 1
        else:
            self.menu_right_panel.addstr(1, 1, f"Equipped:" + (' ' * (x - 2 - len(f"Equipped:"))))
            for i, (k, v) in enumerate(self.player['inventory']['equipped'].items()):
                if i > my - 2:
                    break
                self.menu_right_panel.addstr(i, 1, f"{k}: {v['name']}" + (' ' * (x - 2 - len(f"{k}: {v['name']}"))))
            self.menu_right_panel.refresh()

    def update(self, grid, player, text):
        self.player = player
        self.grid_world = grid
        self.call_panels()
        if self.welcome_text:
            self.text_pan("Welcome to the game!")
            self.welcome_text = False
        if text is not None and len(text) >= 5: #is not None:
            self.text_pan(text)
        if self.player is not None and self.grid_world is not None:
            self.player_pan()
            self.tile_pan()
            self.draw_screen()
        self.refresh_panels()
    
    def create_tile(self, tile):
        if tile.id == 'object':
            if tile.object['id'] == 4:
                id = data.WALL[tile.object['tier']]
            else:
                id = data.OBJ[tile.object['id']]
        elif tile.id == 'entity':
            id = data.ENT[tile.entity.id]
        else:
            id = '.'
        
        if tile.entity is not None and tile.entity.pid == self.player['pid']:
            cell, color = self.create_player_tile(self.player, tile)
        else:
            cell = id
            color = self.get_color(tile)
        return cell, color
    
    def create_player_tile(self, player, tile):
        cell = data.PLR[player['direction']]
        bg = data.BG['black']
        if tile.items != [] and tile.items is not None:
            bg = data.BG['magenta']
        color = data.FG['cyan'] + bg
        return cell, color

    def get_color(self, tile):
        fg = data.FG['white']
        bg = data.BG['black']

        if tile.id != None:
            if tile.object is not None:
                object = tile.object
                if object['id'] != 4:
                    if object['tier'] == 1:
                        fg = data.FG['white']
                        return fg + bg
                    elif object['tier'] == 2:
                        fg = data.FG['green']
                        return fg + bg
                    elif object['tier'] == 3:
                        fg = data.FG['yellow']
                        return fg + bg
                    elif object['tier'] == 4:
                        fg = data.FG['red']
                        return fg + bg
                    elif object['tier'] == 5:
                        fg = data.FG['green']
                        bg = data.BG['cyan']
                        return fg + bg
                    elif object['tier'] == 6:
                        fg = data.FG['yellow']
                        bg = data.BG['cyan']
                        return fg + bg
                    elif object['tier'] == 7:
                        fg = data.FG['red']
                        bg = data.BG['cyan']
                        return fg + bg
                    elif object['tier'] == 8:
                        fg = data.FG['magenta']
                        bg = data.BG['cyan']
                        return fg + bg
                    else:
                        fg = data.FG['white']
                        return fg + bg

            if tile.entity is not None:
                entity = tile.entity
                if tile.id == 'entity':
                    if entity.combat_level > self.player['combat_level']:
                        fg = data.FG['red']
                    elif entity.combat_level == self.player['combat_level']:
                        fg = data.FG['yellow']
                    elif entity.combat_level < self.player['combat_level']:
                        fg = data.FG['green']

            if tile.items != [] and tile.items is not None:
                bg = data.BG['magenta']
                if tile.object is None and tile.entity is None:
                        fg = data.FG['black']

        return fg + bg

    def draw_screen(self):
        for x in range(self.grid_world.shape[0]):
            for y in range(self.grid_world.shape[1]):
                new_tile = self.grid_world[x][y]
                if self.last_grid is not None:
                    old_tile = self.last_grid[x][y]
                    if new_tile != old_tile:
                        tile, color = self.create_tile(new_tile)
                        self.screen_panel.addch(x, y * 2, tile, curses.color_pair(color))
                        self.screen_panel.refresh()
                else:
                    tile, color = self.create_tile(new_tile)
                    self.screen_panel.addch(x, y * 2, tile, curses.color_pair(color))
                    self.screen_panel.refresh()
        self.last_grid = self.grid_world

    def call_panels(self):
        # # self.screen_panel.clear()
        # self.text_panel.clear()
        # self.menu_right_panel.clear()
        # self.menu_left_panel.clear()
        self.text_panel.box()
        self.menu_right_panel.box()
        self.menu_left_panel.box()

    def refresh_panels(self):
        # self.screen_panel.refresh()
        self.text_panel.refresh()
        self.menu_right_panel.refresh()
        self.menu_left_panel.refresh()
    
    def get_area_of_tiles(self, distance):
        x, y = self.player['local_x'], self.player['local_y']
        tiles = []
        for i in range(-distance, distance + 1):
            for j in range(-distance, distance + 1):
                tiles.append((x + i, y + j))
        return tiles
    
    def get_target_tile(self):
        x, y = self.player['local_x'], self.player['local_y']
        if self.player['direction'] == 'up':
            x -= 1
        elif self.player['direction'] == 'down':
            x += 1
        elif self.player['direction'] == 'left':
            y -= 1
        elif self.player['direction'] == 'right':
            y += 1
        return x, y

    def player_pan(self):
        y, x = self.menu_left_panel.getmaxyx()
        if not self.flag:
            self.menu_left_panel.addstr(1, 1, f"Player: {self.player['name']}")
            self.menu_left_panel.addstr(2, 1, f"Health: {self.player['health']}/{self.player['max_health']}            ")
            self.menu_left_panel.addstr(3, 1, f"Combat Level: {self.player['combat_level']}      ")
        else:
            self.menu_left_panel.addstr(1, 1, f"Inventory:"                  )
            for i, item in enumerate(self.player['inventory']['slots']):
                self.menu_left_panel.addstr(i+2, 1, f"{item['name']}: {item['quantity']}" + (' ' * (x - 2 - len(f"{item['name']}: {item['quantity']}"))))
        self.menu_left_panel.refresh()


    def text_pan(self, text):
        y, x = self.text_panel.getmaxyx()
        if text is not None:
            self.text_queue.append(text)
        if len(self.text_queue) > y - 2:
            self.text_queue.pop(0)
        # self.text_panel.clear()
        self.text_panel.box()
        for i, line in enumerate(self.text_queue):
            if len(line) > x - 2:
                line = line[:x - 2]
            self.text_panel.addstr(i+1, 1, line + ' ' * (x - 2 - len(line)))
        self.text_panel.refresh()


    def close(self):
        curses.endwin()

class Client:
    def __init__(self, config):
        self.config = config
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((config["host"], int(config["port"])))
        self.render = Renderer()
        self.button_handler = ButtonHandler()
        self.response = None
        self.login_array = None
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
                    player = req['data']['player']
                    grid = pickle.loads(base64.b64decode(req['data']['client_view'].encode('utf-8')))
                    text = req['data']['text']
                    self.render.update(grid, player, text)


            except (ConnectionResetError, struct.error) as e:
                print(str(e))
                break

    def handle_input(self, stdscr):
        stdscr.nodelay(True)
        stdscr.timeout(100)  # Add this line to set a timeout for getch
        y, x = stdscr.getmaxyx()
        # resize = curses.is_term_resized(y, x)
        while True:
            resize = curses.is_term_resized(y, x)
            if resize is True:
                y, x = stdscr.getmaxyx()
                stdscr.clear()
                curses.resizeterm(y, x)
                self.resize(stdscr)
                stdscr.refresh()
            command = stdscr.getch()
            if command == -1:
                continue
            action = self.button_handler.handle_button_press(chr(command), self.render)
            if chr(command) == 'q':
                packet = self.create_packet('move', {'move': action})
                self.client.sendall(packet)
                self.close(stdscr)
                break
            if action is not None:
                packet = self.create_packet('move', {'move': action})
                self.client.sendall(packet)
            # if chr(command) == 'e':
            #     if self.render.flag:
            #         self.render.flag = False
            #     else:
            #         self.render.flag = True

    def resize(self, stdscr):
        height, width = stdscr.getmaxyx()
        screen_width = width // 2
        qwidth = width // 4
        text_height = height // 2

        self.screen_panel = curses.newwin(height, screen_width, 0, 0)
        self.menu_right_panel = curses.newwin(text_height, qwidth, 0, screen_width + qwidth)
        self.menu_left_panel = curses.newwin(text_height, qwidth, 0, screen_width)
        self.text_panel = curses.newwin(text_height, screen_width, text_height, screen_width)

    def main(self, stdscr):
        self.init_colors()
        self.login(stdscr)
        self.render.init_curses(stdscr)
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()
        self.handle_input(stdscr)

    def login_animation(self, stdscr, screen_hight, screen_width, ch, cw, center):

        for x in range(self.login_array.shape[0]):
            for y in range(self.login_array.shape[1]):
                if screen_hight <= x < screen_hight + ch and screen_width <= y < screen_width + cw:
                    continue
                self.login_array[x, y] = random.choice([21, 31, 41,])# , 71, 81 11,  51, 61
                color = self.login_array[x, y]
                stdscr.addch(x, y, f' ', curses.color_pair(int(color)))
        stdscr.refresh()
        center.box()
        center.addstr(1, (cw-6)//2, f'Log in')
        center.addstr(4, 1, 'Username: ')
        center.addstr(6, 1, 'Password: ')
        center.refresh()

    def login(self, stdscr):
        height, width = stdscr.getmaxyx()
        screen_width = width // 3
        screen_hight = height // 3
        if self.login_array is None:
            self.login_array = np.zeros((height-1, width-1))
        center = curses.newwin(screen_hight, screen_width, screen_hight, screen_width)
        ch, cw = center.getmaxyx()
        username_win = curses.newwin(1, cw - 12, screen_hight + 4, screen_width + 11)
        password_win = curses.newwin(1, cw - 12, screen_hight + 6, screen_width + 11)
        username_box = curses.textpad.Textbox(username_win)
        password_box = curses.textpad.Textbox(password_win)
        self.login_animation(stdscr, screen_hight, screen_width, ch, cw, center)

        curses.echo() 
        curses.nocbreak()
        self.username = username_box.edit().rstrip()
        username_win.refresh()
        self.password = password_box.edit().rstrip()
        # win.addstr(2, 12, "*" * len(username))  # Masking password
        password_win.refresh()
        curses.cbreak()
        curses.noecho()
        packet = self.create_packet('login', {'username': self.username, 'password': self.password})
        self.client.sendall(packet)

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

    def close(self, stdscr):
        curses.nocbreak()
        curses.echo()
        stdscr.keypad(0)
        curses.endwin()
        self.client.close()

class ButtonHandler:
    def __init__(self):
        self.game_button = {
            'w': 'up',
            'a': 'left',
            's': 'down',
            'd': 'right',
            'q': 'quit',
            'f': 'interact',
            # 'r': 'toggle_panel',
            'e': 'attack',
        }
        self.client_button = {
            'r': 'toggle_panel'
        }


    def handle_button_press(self, command, renderer):
        if command in self.game_button:
            return self.game_button.get(command, None)
        else:
            com = self.client_button.get(command, None)
            if com is not None:
                self.handle_client_button_press(com, renderer)
    
    def handle_client_button_press(self, com, render):
        if com == 'toggle_panel':
            if render.flag:
                render.flag = False
            else:
                render.flag = True
    
if __name__ == "__main__":
    client = Client()
    curses.wrapper(client.main)


# Curses Dynamic Resizing?
# # Initialize the screen
# import curses

# screen = curses.initscr()

# # Check if screen was re-sized (True or False)
# resize = curses.is_term_resized(y, x)

# # Action in loop if resize is True:
# if resize is True:
#     y, x = screen.getmaxyx()
#     screen.clear()
#     curses.resizeterm(y, x)
#     screen.refresh()


