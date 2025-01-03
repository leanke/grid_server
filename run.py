import argparse
import configparser
import grid_server.server as server
import grid_client.client as client

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def main():
    config = load_config()
    parser = argparse.ArgumentParser(description="Run the GridWorld server or client.")
    parser.add_argument('--mode', choices=['server', 'client'], default='client', help="'server' or 'client'")
    parser.add_argument('--port', default=config['client']['port'], help="Port to run the server on")
    parser.add_argument('--host', default=config['client']['host'], help="Host to connect to")
    parser.add_argument('--world', default=config['server']['world_name'], help="World name")
    args = parser.parse_args()

    if args.mode == 'server':
        if args.port:
            config['server']['port'] = args.port
        if args.world:
            config['server']['world_name'] = args.world
        if args.host:
            config['server']['host'] = args.host
        server_instance = server.GameServer(config['server'])
        try:
            server_instance.start()
        except KeyboardInterrupt:
            server_instance.stop()
    elif args.mode == 'client':
        if args.port:
            config['client']['port'] = args.port
        if args.host:
            config['client']['host'] = args.host
        client_instance = client.Client(config['client'])
        client_instance.main()

if __name__ == "__main__":
    main()