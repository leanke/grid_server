import json
import socket
import struct
import threading
import numpy as np
import tty
import termios
import sys
import curses

COLOR = {
    'WHITE': ' ',
    'BLACK': '█',
    'GREEN': 'G',
    'BLUE': 'B',
    'RED': 'R',
    'YELLOW': 'Y',
    'CYAN': 'C',
    'MAGENTA': 'M',
    'GRAY': '.',
}

ID = {
    "up": '˄',
    "down": '˅',
    "left": '˂',
    "right": '˃',
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
        self.grid_world = []
        self.text_queue = []
        self.flag = False


    def screen(self, screen, player_id, screen_panel):
        for row in screen:
            row_print = []
            for cell in row:
                if cell['id'] == 3:
                    if int(cell['attributes']['base']['id']) == int(player_id):
                        row_print.append(ID[cell['attributes']['direction']])
                    else:
                        row_print.append(ID[cell['id']])
                else:
                    row_print.append(ID[cell['id']])


            screen_panel.addstr(' '.join([val for val in row_print]) + '\n')


    def menu(self, menu, menu_right_panel, menu_left_panel):
        # menu = {
        #     'base': {'id': 1000001, 'name': 'leanke', 'type': 'Dev'}, 
        #     'coords': {'x': 14, 'y': 13}, 
        #     'direction': 'left', 
        #     'skills': {'attack': 1, 'defence': 1, 'health': 1, 'woodcutting': 1, 'mining': 1, 'firemaking': 1}, 
        #     'xp': {'attack': 0, 'defence': 0, 'health': 0, 'woodcutting': 0, 'mining': 0, 'firemaking': 0}, 
        #     'max_health': 10, 
        #     'health': 10, 
        #     'inventory': [
        #         {'id': 7, 'name': 'Axe', 'description': 'An Axe', 'level': 1, 'value': 20, 'damage': 1}, 
        #         {'id': 3, 'name': 'Staff', 'description': 'A Staff', 'level': 1, 'value': 20, 'damage': 1}
        #         ], 
        #     'combat_level': 1, 
        #     'tile': {'id': 1, 'attributes': {'type': 'tree', 'health': 5, 'mod': None, 'resource': 'logs'}}}
        if menu['tile']['id'] != 0:
                self.tile(menu, menu_right_panel)
        else:
            self.inventory(menu['inventory'], menu_right_panel)
            
        if self.flag:
            self.skills(menu['skills'], menu_left_panel)
        else:
            self.player(menu, menu_left_panel)

    def text(self, text, text_panel):
        self.text_queue.append(text)
        if len(self.text_queue) > 13:
            self.text_queue.pop(0)
        for i, text in enumerate(self.text_queue):
            text_panel.addstr(i+1, 1, self.text_queue[i])
         
    def tile(self, menu, tile_panel):
        if menu['tile']['id'] == 3:
            player = menu['tile']['attributes']
            tile_panel.addstr(1, 1, f"{player['base']['name']}:")
            tile_panel.addstr(2, 1, f"  Combat Level: {player['combat_level']}")
            tile_panel.addstr(3, 1, f"  Health: {player['health']}")
            tile_panel.addstr(4, 1, f"  Type: {player['base']['type']}")
        elif menu['tile']['id'] == 4:
            tile_panel.addstr(1, 1, "Wall:")
            tile_panel.addstr(2, 1, "  Impassable")
        else:
            tile_type = menu['tile']['attributes']['type']
            if menu['tile']['attributes']['mod'] is not None:
                tile_type = menu['tile']['attributes']['mod'] + ' ' + menu['tile']['attributes']['type']
            tile_panel.addstr(1, 1, f"{tile_type}:")
            tile_panel.addstr(2, 1, f"  Health: {menu['tile']['attributes']['health']}")
            tile_panel.addstr(3, 1, f"  Resource: {menu['tile']['attributes']['resource']}")

    def player(self, menu, player_panel):
        player_panel.addstr(1, 1, f"Player: {menu['base']['name']}")
        player_panel.addstr(2, 1, f"Health: {menu['health']}/{menu['max_health']}")
        player_panel.addstr(3, 1, f"Combat Level: {menu['combat_level']}")

    def skills(self, skills, skills_panel):
        skills_panel.addstr(1, 1, "Skills:")
        skills_panel.addstr(2, 1, f"  Attack: {skills['attack']}")
        skills_panel.addstr(3, 1, f"  Defence: {skills['defence']}")
        skills_panel.addstr(4, 1, f"  Health: {skills['health']}")
        skills_panel.addstr(5, 1, f"  Woodcutting: {skills['woodcutting']}")
        skills_panel.addstr(6, 1, f"  Mining: {skills['mining']}")
        skills_panel.addstr(7, 1, f"  Firemaking: {skills['firemaking']}")
    
    def inventory(self, inventory, inventory_panel):
        inventory_panel.addstr(1, 1, "Inventory:")
        for i, item in enumerate(inventory):
            inventory_panel.addstr(i+2, 1, f"  {item['name']}")

class Client:
    def __init__(self, config):
        self.config = config
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((config["host"], int(config["port"])))
        self.renderer = GridWorldRenderer()
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

    def receive_data(self, screen_panel, text_panel, menu_right_panel, menu_left_panel):
        self.call_panels(screen_panel, text_panel, menu_right_panel, menu_left_panel)
        while True:
            try:
                header = self.client.recv(4)
                if not header:
                    break
                data = self.unpack_packet(header)
                req = json.loads(data.decode('utf-8'))

                if req['type'] == 'game_state':
                    if req['data']['screen'] is not None and req['data']['menu'] is not None:
                        screen_panel.clear()
                        self.renderer.screen(req['data']['screen'], req['data']['menu']['base']['id'], screen_panel)
                    if req['data']['menu'] is not None:
                        menu_right_panel.clear()
                        menu_right_panel.box()
                        menu_left_panel.clear()
                        menu_left_panel.box()
                        self.renderer.menu(req['data']['menu'], menu_right_panel, menu_left_panel)
                    if req['data']['text'] is not None:
                        text_panel.clear()
                        text_panel.box()
                        self.renderer.text(req['data']['text'], text_panel)

                    screen_panel.refresh()
                    menu_right_panel.refresh()
                    menu_left_panel.refresh()
                    text_panel.refresh()

            except (ConnectionResetError, struct.error) as e:
                print(str(e))
                break

    def handle_input(self, stdscr):
        stdscr.nodelay(True)
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
                if self.renderer.flag:
                    self.renderer.flag = False
                else:
                    self.renderer.flag = True

    def login(self):
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")
        packet = self.create_packet('login', {'username': self.username, 'password': self.password})
        self.client.send(packet)

    def main(self):
        self.login()
        curses.wrapper(self.curses_main)

    def curses_main(self, stdscr):

        curses.curs_set(0)
        height, width = stdscr.getmaxyx()
        screen_width = width // 2
        qwidth = width // 4
        text_height = height // 2

        screen_panel = curses.newwin(height, screen_width, 0, 0)
        menu_right_panel = curses.newwin(text_height, qwidth, 0, screen_width+qwidth)
        menu_left_panel = curses.newwin(text_height, qwidth, 0, screen_width)
        text_panel = curses.newwin(text_height, screen_width, text_height, screen_width)

        receive_thread = threading.Thread(target=self.receive_data, args=(screen_panel, text_panel, menu_right_panel, menu_left_panel))
        receive_thread.start()

        self.handle_input(stdscr)

    def call_panels(self, screen_panel, text_panel, menu_right_panel, menu_left_panel):
        screen_panel.clear()
        text_panel.clear()
        menu_right_panel.clear()
        menu_left_panel.clear()
        text_panel.box()
        menu_right_panel.box()
        menu_left_panel.box()
        screen_panel.refresh()
        text_panel.refresh()
        menu_right_panel.refresh()
        menu_left_panel.refresh()

    def close(self):
        self.client.close()
        sys.exit()

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
