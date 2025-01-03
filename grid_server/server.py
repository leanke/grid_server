import socket
import os
import threading
import json
import time

from grid_server.classes.environment import GridWorld
from grid_server.classes.player import Player


class GameServer:
    def __init__(self, config):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((config["host"], int(config["port"])))
        self.server.listen(5)
        print(f"Server started on {config['host']}:{config['port']}")
        self.clients = []
        self.path = f"./grid_server/worlds/{config['world_name']}"
        self.config = config
        if not os.path.exists(self.path):
            config['new_world'] = 'True'
            self.create_world_files()
        else:
            config['new_world'] = 'False'
        self.grid_world = GridWorld((130,130), self.path)
        self.grid_world.grid.load_world()
        self.player_list = set()
        self.running = True

    def create_world_files(self):
        userpath = self.path + '/users/'
        logpath = self.path + '/logs/'
        os.makedirs(self.path)
        os.system(f"touch {self.path}/game_state.npy")
        os.makedirs(userpath)
        os.makedirs(logpath)
    
    def create_packet(self, type, data):
        packet_format = {
            'type': 'none',
            'data':  {}
        }
        packet_format['data'] = data
        packet_format['type'] = type
        packet = json.dumps(packet_format).encode('utf-8')
        length = len(packet).to_bytes(4, byteorder='big')
        # print(f'Pack: {packet}')
        return length + packet

    def unpack_packet(self, packet):
        length = int.from_bytes(packet[:4], byteorder='big')
        data = json.loads(packet[4:length+4].decode('utf-8'))
        # print(f'Unpack: {data}')
        return data

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024)
            if not data:
                return
            req = self.unpack_packet(data)
            username = req['data']['username']
            password = req['data']['password']
            player = self.get_or_create_player(username, password)

            if req['type'] == 'login':
                self.send_game_state(client_socket, None)
            while self.running:
                command = client_socket.recv(1024)
                if not command:
                    break
                unpacked_data = self.unpack_packet(command)
                ret = {}

                if unpacked_data['data']['move'] == 'quit':
                    player.save()
                    self.grid_world.grid.remove(player.x, player.y)
                    print(f"Player {player.name} disconnected")
                    self.player_list.remove(player)
                    if client_socket in self.clients:
                        self.clients.remove(client_socket)
                    break
                elif unpacked_data['data']['move']:
                    retu = self.grid_world.step(player, unpacked_data['data']['move'])
                    
                    ret = retu
                
                self.send_game_state(client_socket, ret)
        except ConnectionResetError:
            pass
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()

    def get_or_create_player(self, username, password):
        path = f'{self.path}/users/{username}'
        if not os.path.exists(f'{path}.json'):
            player = self.create_player(username, password, path)
        else:
            with open(f'{path}.json') as f:
                config = json.load(f)
                player = Player(config, path)
        if password != player.password:
            player = None
        self.player_list.add(player)
        return player

    def create_player(self, username, password, path):
        os.system(f"touch {path}.json")
        os.system(f"cp ./grid_server/default.json {path}.json")
        _, _, files = next(os.walk(f'{self.path}/users/'))
        file_count = len(files)
        with open(f'{path}.json') as f:
                    config = json.load(f)
                    player = Player(config, path)
        player.name = username
        player.password = password
        player.id = 1_000_000 + file_count
        player.save()
        return player

    def send_game_state(self, client_socket, data):
        if data is not None:
            data['screen'] = data['screen'].tolist()

            packet = self.create_packet('game_state', data)
            try:
                client_socket.sendall(packet)
            except socket.error as e:
                print(f"Error sending data: {e}")
                self.clients.remove(client_socket)
                client_socket.close()

    def broadcast_game_state(self):
        for client in self.clients:
            self.send_game_state(client, data=None)

    def tick(self):
        tick = 0
        while self.running:
            tick += 1
            # if tick % 100 == 0:
            #     print(self.player_list)
            # Update the game world
            self.grid_world.step(None, None)
            self.broadcast_game_state()
            time.sleep(0.1)

    def start(self):
        # Start the tick loop in a separate thread
        tick_thread = threading.Thread(target=self.tick)
        tick_thread.start()

        while self.running:
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




