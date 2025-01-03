import socket
import os
import threading
import json
import time

from grid_server.classes.environment import GridWorld
from grid_server.classes.player import Player


class GameServer:
    def __init__(self, config):
        """
        Initialize the game server with the given configuration.
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((config["host"], int(config["port"])))
        self.server.listen(5)
        print(f"Server started on {config['host']}:{config['port']}")
        self.clients = []
        self.client_player = {}
        self.path = f"./grid_server/worlds/{config['world_name']}"
        self.config = config
        if not os.path.exists(self.path):
            config['new_world'] = 'True'
            self.create_world_files()
        else:
            config['new_world'] = 'False'
        self.grid_world = GridWorld(self.path)
        self.player_list = set()
        self.running = True

    def create_world_files(self):
        """
        Create necessary files and directories for a new world.
        """
        userpath = self.path + '/users/'
        logpath = self.path + '/logs/'
        os.makedirs(self.path)
        os.makedirs(userpath)
        os.makedirs(logpath)
    
    def create_packet(self, type, data):
        """
        Create a packet to send to the client.
        """
        packet_format = {
            'type': type,
            'data': data
        }
        packet = json.dumps(packet_format).encode('utf-8')
        length = len(packet).to_bytes(4, byteorder='big')
        return length + packet

    def unpack_packet(self, packet):
        """
        Unpack a received packet from the client.
        """
        length = int.from_bytes(packet[:4], byteorder='big')
        data = json.loads(packet[4:length+4].decode('utf-8'))
        return data

    def handle_client(self, client_socket):
        """
        Handle communication with a connected client.
        """
        try:
            data = client_socket.recv(1024)
            if not data:
                return
            req = self.unpack_packet(data)
            username = req['data']['username']
            password = req['data']['password']
            player = self.get_or_create_player(username, password)

            if req['type'] == 'login':
                self.send_game_state(client_socket, player, None)
                self.clients.append(client_socket)
                self.client_player[client_socket] = player
            while self.running:
                command = client_socket.recv(1024)
                if not command:
                    break
                unpacked_data = self.unpack_packet(command)
                ret = {}

                if unpacked_data['data']['move'] == 'quit':
                    self.handle_quit(client_socket, player)
                    break
                elif unpacked_data['data']['move']:
                    ret = self.grid_world.step(player, unpacked_data['data']['move'])
                
                self.send_game_state(client_socket, player, ret)
        except ConnectionResetError:
            pass
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()

    def handle_quit(self, client_socket, player):
        """
        Handle player quitting the game.
        """
        player.save()
        self.grid_world.grid.remove(player.x, player.y)
        print(f"Player {player.name} disconnected")
        self.player_list.remove(player)
        if client_socket in self.clients:
            self.clients.remove(client_socket)

    def get_or_create_player(self, username, password):
        """
        Get an existing player or create a new one.
        """
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
        """
        Create a new player.
        """
        os.system(f"touch {path}.json")
        os.system(f"cp ./grid_server/default.json {path}.json")
        _, _, files = next(os.walk(f'{self.path}/users/'))
        file_count = len(files)
        with open(f'{path}.json') as f:
            config = json.load(f)
            player = Player(config, path)
        player.name = username
        player.password = password
        player.pid = 1_000_000 + file_count
        player.save()
        return player

    def send_game_state(self, client_socket, player, data):
        """
        Send the current game state to the client.
        """
        if data is not None:
            menu = player.player_data()
            menu['tile'] = self.grid_world.tile_info(player)
            data['menu'] = menu
            data['screen'] = data['screen'].tolist()
            packet = self.create_packet('game_state', data)
        else:
            screen = self.grid_world.grid.client_view(player.x, player.y).tolist()
            packet = self.create_packet('game_state', {'screen': screen, 'text': None, 'menu': None})
        try:
            client_socket.sendall(packet)
        except socket.error as e:
            print(f"Error sending data: {e}")
            self.clients.remove(client_socket)
            client_socket.close()

    def broadcast_game_state(self):
        """
        Broadcast the game state to all connected clients.
        """
        for client in self.clients:
            player = self.client_player[client]
            self.send_game_state(client, player, data=None)

    def tick(self):
        """
        Main game loop to update the game world.
        """
        tick = 0
        while self.running:
            tick += 1
            self.grid_world.step(None, None)
            self.broadcast_game_state()
            time.sleep(0.5)

    def start(self):
        """
        Start the game server.
        """
        tick_thread = threading.Thread(target=self.tick)
        tick_thread.start()

        while self.running:
            client_socket, addr = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def stop(self):
        """
        Stop the game server.
        """
        self.grid_world.close()
        self.running = False
        self.server.close()

if __name__ == "__main__":
    server = GameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()




