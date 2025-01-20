import socket
import os
import threading
import json
import time
import uuid

from grid_server.classes.environment import GridWorld
from grid_server.classes.entities.player import Player
from grid_server.classes.data import new_player


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
        packet = {
            'type': type if type is not None else 'none',
            'data': data if data is not None else {}
        }
        packet = json.dumps(packet).encode('utf-8')
        length = len(packet).to_bytes(4, byteorder='big')
        return length + packet

    def unpack_packet(self, header, client_socket):
        data_length = int.from_bytes(header, byteorder='big')
        data = b''
        while len(data) < data_length:
            packet = client_socket.recv(data_length - len(data))
            if not packet:
                break
            data += packet
        return data

    def handle_client(self, client_socket):
        """
        Handle communication with a connected client.
        """
        try:
            header = client_socket.recv(4)
            if not header:
                return
            data = self.unpack_packet(header, client_socket)
            req = json.loads(data.decode('utf-8'))



            # data = client_socket.recv(1024)
            if not req:
                return
            # req = self.unpack_packet(data)
            username = req['data']['username']
            password = req['data']['password']
            player = self.get_or_create_player(username, password)
            # print(player)

            if req['type'] == 'login':
                self.send_game_state(client_socket, player, None)
                self.clients.append(client_socket)
                self.client_player[client_socket] = player
            while self.running:

                header = client_socket.recv(4)
                if not header:
                    return
                data = self.unpack_packet(header, client_socket)
                unpacked_data = json.loads(data.decode('utf-8'))

                ret = {}

                if unpacked_data['data']['move'] == 'quit':
                    self.handle_quit(client_socket, player)
                    break
                elif unpacked_data['data']['move']:
                    if player is not None:
                        print(f"Player {player.name} moved {unpacked_data['data']['move']}")
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
        self.grid_world.grid.remove(player.x, player.y, 'entity')
        print(f"Player {player.name} disconnected")
        self.player_list.remove(player)
        if client_socket in self.clients:
            self.clients.remove(client_socket)

    def get_or_create_player(self, username, password):
        """
        Get an existing player or create a new one.
        """
        path = f'{self.path}/users/{username}'
        print(username, password)
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
        with open(f'{path}.json', 'w') as f:
            json.dump(self.create_base_player(username, password), f, indent=4)
        with open(f'{path}.json') as f:
            config = json.load(f)
            player = Player(config, path)
        player.save()
        return player
    
    def create_base_player(self, username, password):
        new_player["base"]["pid"] = f'{str(uuid.uuid4())[:8]}'
        new_player["base"]["name"] = f'{str(username)}'
        new_player["base"]["password"] = f'{str(password)}'
        return new_player

    def send_game_state(self, client_socket, player, data):
        """
        Send the current game state to the client.
        """
        if player is not None:
            array, _ = self.grid_world.grid.client_view(player)
            pack = {
                'player': player.client_data(),
                'client_view': array,
                'text': None,
            }
            if data is not None:
                pack['text'] = data

            packet = self.create_packet('game_state', pack)
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
            time.sleep(0.1)

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
    pass







