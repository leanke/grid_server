# grid_server
A basic server and client in Python.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/leanke/grid_server.git
    ```

2. Install the package:
    ```sh
    pip install -e ./grid_server
    ```

## Controls

- **W, A, S, D**: Move Up, Left, Down, Right
- **F**: Interact with the tile in front of the player
- **E**: Toggle client panel
- **Q**: Quit

## Running

To start the server:
```sh
python run.py --mode server
```

To run the client:
```sh
python run.py --mode client
```
