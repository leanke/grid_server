import base64
import json
import socket
import os
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
        self.button_handler = ButtonHandler()

    def send_command(self, command):
        self.client.send(command.encode('utf-8'))

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

        while True:
            try:
                header = client.recv(8)
                if not header:
                    break
                data_length, checksum = struct.unpack('!II', header)
                data = b""
                while len(data) < data_length:
                    packet = client.recv(data_length - len(data))
                    if not packet:
                        break
                    data += packet

                if data:
                    if zlib.crc32(data) != checksum:
                        error = "Checksum mismatch, data corrupted"
                        self.print_pane(bottom_right_pane, error)
                        continue

                    try:
                        data_rec = data.decode('utf-8')
                        unpacked_data = json.loads(data_rec)

                        screen_data_b64 = unpacked_data.get("screen")
                        if screen_data_b64:
                            screen_data = base64.b64decode(screen_data_b64)
                            screen_array = np.frombuffer(screen_data, dtype=np.uint8)
                            screen_array = screen_array.reshape(int(self.config['grid_size']), int(self.config['grid_size']))
                            self.renderer.render(screen_array, left_pane)

                        text = unpacked_data.get("text", "")
                        if text:
                            self.print_pane(bottom_right_pane, text)

                        left_pane.refresh()
                        top_right_pane.refresh()
                        bottom_right_pane.refresh()

                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        error_message = f"Error decoding data: {e}"
                        self.print_pane(bottom_right_pane, error_message)
                        print(f"Raw data: {data}")
                        continue
            except (ConnectionResetError, struct.error) as e:
                print(f"Connection error: {e}")
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
                    client.send(action.encode('utf-8'))
                if command == 'q':
                    self.close()
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def create_user(self):
        create = input("Player does not exist. Create new player? (y/n): ")
        self.client.send(create.encode('utf-8'))
        response = self.client.recv(1024).decode('utf-8')
        if response == 'USER_CREATED':
            print("Player created successfully.")
        else:
            print("Player creation aborted.")
            self.close()
            sys.exit()

    def login(self):
        self.username = input("Enter your username: ")
        self.client.send(self.username.encode('utf-8'))
        response = self.client.recv(1024).decode('utf-8')
        if response == 'USER_NOT_FOUND':
            self.create_user()
        elif response == 'USER_CREATION_ABORTED':
            print("Player creation aborted.")
            self.close()
            sys.exit()
        elif response == 'USER_FOUND':
            self.renderer = GridWorldRenderer()

    def main(self):
        self.login()
        receive_thread = threading.Thread(target=curses.wrapper, args=(self.receive_data, self.client))
        receive_thread.start()

        self.handle_input(None, self.client)
        # self.login()
        # receive_thread = threading.Thread(target=curses.wrapper, args=(self.receive_data, self.client))
        # receive_thread.start()

        # self.handle_input(None, self.client)

    def close(self):
        self.client.close()



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
