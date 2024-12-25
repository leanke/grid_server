import base64
import socket
import os
import threading
import json
import time
import numpy as np
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

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024)
            req = self.unpack_packet(data)
            username = req['data']['username']
            password = req['data']['password']
            path = self.userpath + username

            if not os.path.exists(f'{path}.ini'):
                player = self.create_player(username, password, path)
                print(f"Creating account for {username}")
                response = self.create_packet('success', {'data': f'Account created for {username}'}) 
            else:
                player = Player(f'{path}.ini')
                
                
            if req['type'] == 'login':
                if player.get('base', 'password') == password:
                    print(f"{username} has logged in")
                    response = self.create_packet('success', {'data': f'Logging into: {username}'})
                else:
                    response = self.create_packet('fail', {'data': f'Username or password is incorrect'})
            else:
                response = self.create_packet('fail', {'data': f'Account not created for {username}'}) 
            
            client_socket.sendall(response)

            while True:
                command = client_socket.recv(1024)
                unpacked_data = self.unpack_packet(command)
                print(unpacked_data)
                player = Player(f'{path}.ini') # make an attr of the class instead of relying on the file
                print(player.name, player.x, player.y)
                ret = None
                if unpacked_data['data']['move'] == 'quit': # this conditional breaks the client quitting gracefully? maybe .sendall a 'quit' packet?
                    print(f"Player {username} disconnected")
                    self.grid_world.grid.remove(player.x, player.y)
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
                elif unpacked_data['data']['move']:
                    ret = self.grid_world.step(player, unpacked_data['data']['move'])
                else:
                    ret = 'Invalid command'

                self.send_game_state(client_socket, ret)
        except ConnectionResetError:
            pass
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    def create_player(self, username, password, path):
        os.system(f"touch {path}.ini")
        os.system(f"cp ./grid_server/default.ini {path}.ini")
        player = Player(f'{path}.ini')
        player.save('base', 'name', username)
        player.save('base', 'password', password)
        return player

    def send_game_state(self, client_socket, data):
        state = self.grid_world.grid.game
        screen_data = np.array(state).tobytes()
        encoded_screen_data = base64.b64encode(screen_data).decode('utf-8')
        game_state_packet = {
            'screen': encoded_screen_data,
            'text': data,
        }
        packet = self.create_packet('game_state', game_state_packet)
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
        while self.running:
            # Update the game world
            self.grid_world.step(None, None)
            self.broadcast_game_state()
            time.sleep(0.1)

    def start(self):
        # Start the tick loop in a separate thread
        tick_thread = threading.Thread(target=self.tick)
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