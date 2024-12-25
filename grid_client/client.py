import base64
import json
import socket
import struct
import threading
import numpy as np
from grid_client.render import GridWorldRenderer
import tty
import termios
import sys
import curses
import zlib

class Client:
    def __init__(self, config, host='localhost', port=12345):
        self.config = config
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.response = None
        self.renderer = GridWorldRenderer()  # Assuming this is where the game rendering is managed
        self.username = None
        self.password = None
        self.button_handler = ButtonHandler()

    def create_packet(self, type, data):
        packet = {
            'type': type,
            'data': data
        }
        packet = json.dumps(packet).encode('utf-8')
        length = len(packet).to_bytes(4, byteorder='big')
        return length + packet

    def unpack_packet(self, packet):
        length = int.from_bytes(packet[:4], byteorder='big')
        data = json.loads(packet[4:length+4].decode('utf-8'))
        return data

    def receive_data(self, stdscr, client):
        curses.curs_set(0)
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        left_pane = curses.newwin(height, width // 2, 0, 0)
        left_pane.border()
        top_right_pane = curses.newwin(height // 2, width // 2, 0, width // 2)
        top_right_pane.border()
        bottom_right_pane = curses.newwin(height // 2, width // 2, height // 2, width // 2)
        bottom_right_pane.border()
        # self.renderer = GridWorldRenderer()

        while True:
            try:
                data = client.recv(1024)
                req = self.unpack_packet(data)
                if req['type'] == 'game_state':
                    screen_data_b64 = req['data']['screen']
                    screen_data = base64.b64decode(screen_data_b64)
                    screen_array = np.frombuffer(screen_data, dtype=np.uint8)
                    screen_array = screen_array.reshape(int(self.config['grid_size']), int(self.config['grid_size']))
                    self.renderer.render(screen_array, left_pane)
                if req['data']['text'] is not None:
                    text = req['data']['text']
                    self.print_pane(bottom_right_pane, text)
            
                left_pane.refresh()
                top_right_pane.refresh()
                bottom_right_pane.refresh()
            except (ConnectionResetError, struct.error) as e:
                self.print_pane(bottom_right_pane, e)
                break

    def print_pane(self, pane, text):
        pane.clear()
        pane.border()
        pane.addstr(1, 1, text)
        pane.refresh()

    def handle_input(self, stdscr, client):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                command = sys.stdin.read(1)
                action = self.button_handler.handle_button_press(command)
                if action is not None:
                    packet = self.create_packet('move', {'move': action})
                    # print(packet)
                    client.sendall(packet)
                if action == 'quit':
                    self.close()

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def login(self):
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")
        packet = self.create_packet('login', {'username': self.username, 'password': self.password})
        self.client.send(packet)
        rec = self.client.recv(1024)
        response = self.unpack_packet(rec)
        if response['type'] == 'success':
            # print(response['data']['data'])
            self.renderer = GridWorldRenderer()
        elif response['type'] == 'fail':
            print(response['data']['data'])
            self.close()
            


    def main(self):
        self.login()
        receive_thread = threading.Thread(target=curses.wrapper, args=(self.receive_data, self.client))
        receive_thread.start()

        self.handle_input(None, self.client)

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
        else:
            action = None
        return action
    
if __name__ == "__main__":
    Client().main()
