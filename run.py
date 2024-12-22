import argparse
import configparser
import grid_server.server as server
import grid_client.client as client

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def main():
    parser = argparse.ArgumentParser(description="Run the GridWorld server or client.")
    parser.add_argument('--mode', choices=['server', 'client'], default='client', help="'server' or 'client'")
    args = parser.parse_args()

    config = load_config()

    if args.mode == 'server':
        server_instance = server.GameServer(config['server'])
        try:
            server_instance.start()
        except KeyboardInterrupt:
            server_instance.stop()
    elif args.mode == 'client':
        client_instance = client.Client(config['client'])
        client_instance.main()

if __name__ == "__main__":
    main()