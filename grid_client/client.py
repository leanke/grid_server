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
    0: '.',
    1: 'T',
    2: 'R',
    3: 'P',
    4: '█',
    5: '?',
}

class GridWorldRenderer:
    def __init__(self):
        self.grid_world = []

    def render(self, state, window):
        # print(state)
        window.clear()
        # window.box()
        for i, row in enumerate(state):
            window.addstr(' '.join([f'{ID[val]}' for val in row]) + '\n')
        window.refresh()

class Client:
    def __init__(self, config, host='localhost', port=12345):
        self.config = config
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.response = None
        self.renderer = GridWorldRenderer()
        self.username = None
        self.password = None
        self.button_handler = ButtonHandler()

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

    def receive_data(self, screen, text_window, right_panel):
        screen.clear()
        screen.refresh()
        right_panel.clear()
        right_panel.box()
        right_panel.refresh()
        text_window.clear()
        text_window.box()
        text_window.refresh()
        while True:
            try:
                header = self.client.recv(4)
                if not header:
                    break
                data = self.unpack_packet(header)
                req = json.loads(data.decode('utf-8'))
                # print(req['data']['text'])
                
                if req['type'] == 'game_state':
                    if req['data']['screen'] is not None:
                        self.renderer.render(req['data']['screen'], screen)
                    if req['data']['text'] is not None:
                        text_window.clear()
                        text_window.box()
                        text_window.addstr(1, 1, req['data']['text'])
                        text_window.refresh()
                    
                    right_panel.box()
                    right_panel.addstr(1, 1, f"Player: {self.username}")
                    right_panel.refresh()
                    
                
                screen.refresh()
                right_panel.refresh()
                text_window.refresh()
            except (ConnectionResetError, struct.error) as e:
                print(str(e))
                break

    def handle_input(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                command = sys.stdin.read(1)
                action = self.button_handler.handle_button_press(command)
                if command == 'q':
                    packet = self.create_packet('move', {'move': action})
                    self.client.sendall(packet)
                    self.close()
                    break
                if action is not None:
                    packet = self.create_packet('move', {'move': action})
                    self.client.sendall(packet)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

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
        text_height = height // 2

        screen = curses.newwin(height, screen_width, 0, 0)
        right_panel = curses.newwin(text_height, screen_width, 0, screen_width)
        text_window = curses.newwin(text_height, screen_width, text_height, screen_width)
        


        receive_thread = threading.Thread(target=self.receive_data, args=(screen, text_window, right_panel))
        receive_thread.start()

        self.handle_input()

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
        self.inventory = 'e'

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
        elif command == self.inventory:
            action = 'inventory'
        else:
            action = None
        return action
    
if __name__ == "__main__":
    Client().main()
