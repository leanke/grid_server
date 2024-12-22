import base64
import socket
import os
import threading
import json
import time
import numpy as np
from grid_server.classes.environment import GridWorld
from grid_server.classes.player import Player
import struct
import zlib




class GameServer:
    def __init__(self, config):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((config["host"], int(config["port"])))
        self.server.listen(5)
        print(f"Server started on {config['host']}:{config['port']}")
        self.clients = []
        self.path = f"./grid_server/worlds/{config['world_name']}"
        self.userpath = self.path + '/users/'
        self.logpath = self.path + '/logs/'
        config["array_path"] = f"{self.path}/{config['world_name']}.npy"
        self.config = config
        if not os.path.exists(self.path):
            config['new_world'] = 'True'
            self.create_world_files()
        else:
            config['new_world'] = 'False'
        self.path = f"grid_server/{config['world_name']}"
        self.config = config
        self.grid_world = GridWorld(self.config)

        self.running = True

    def create_world_files(self):
        os.makedirs(self.path)
        os.system(f"touch {self.config['array_path']}")
        os.makedirs(self.userpath)
        os.makedirs(self.logpath)

    def handle_client(self, client_socket):
        try:
            # Receive username and load player data
            username = client_socket.recv(1024).decode('utf-8')
            path = self.userpath + username
            if not os.path.exists(f'{path}.ini'):
                client_socket.send(b'USER_NOT_FOUND')
                create_user = client_socket.recv(1024).decode('utf-8')
                if create_user == 'y':
                    os.system(f"touch {path}.ini")
                    os.system(f"cp ./grid_server/default.ini {path}.ini")
                    print(f"Player {username} created")
                    client_socket.send(b'USER_CREATED')
                else:
                    client_socket.send(b'USER_CREATION_ABORTED')
                    return
            else:
                client_socket.send(b'USER_FOUND')
            player = Player(f'{path}.ini')
            print(f"Player {username} connected")
            player.save('base', 'name', username)
            self.clients.append(client_socket)

            while True:
                command = client_socket.recv(1024).decode('utf-8')
                player = Player(f'{path}.ini')
                ret = None
                if command == 'quit':
                    print(f"Player {username} disconnected")
                    self.grid_world.grid.remove(player.x, player.y)
                    break
                if command:
                    ret = self.grid_world.step(player, command)
                self.send_game_state(client_socket, ret)
                # self.send_player_data(client_socket, player, data=f"{player.name}: {ret}")
        except ConnectionResetError:
            pass
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    def send_game_state(self, client_socket, data):
        state = self.grid_world.grid.game
        screen_data = np.array(state).tobytes()
        encoded_screen_data = base64.b64encode(screen_data).decode('utf-8')

        dict_state = {
            'screen': encoded_screen_data,
            'text': data,
        }

        json_data = json.dumps(dict_state)
        data_length = len(json_data)
        checksum = zlib.crc32(json_data.encode('utf-8'))  # Calculate checksum
        header = struct.pack('!II', data_length, checksum)  # 8-byte header: 4 bytes for length, 4 bytes for checksum

        try:
            client_socket.sendall(header)
            client_socket.sendall(json_data.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending data: {e}")
            self.clients.remove(client_socket)
            client_socket.close()

    def broadcast_game_state(self):
        for client in self.clients:
            self.send_game_state(client, data=None)

    def tick_loop(self):
        while self.running:
            # Update the game world
            self.grid_world.step(None, None)
            self.broadcast_game_state()
            time.sleep(0.1)

    def start(self):
        # Start the tick loop in a separate thread
        tick_thread = threading.Thread(target=self.tick_loop)
        tick_thread.start()

        while True:
            client_socket, addr = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def stop(self):
        self.running = False

if __name__ == "__main__":
    server = GameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()