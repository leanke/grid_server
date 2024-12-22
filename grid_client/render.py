import curses

CELL_SIZE = 2  # Each cell is represented with a two-character width in the terminal
GRID_WIDTH = 20
GRID_HEIGHT = 20

COLOR = {
    'WHITE': ' ',
    'BLACK': '█',
    'GREEN': 'G',
    'BLUE': 'B',
    'RED': 'R',
    'YELLOW': 'Y',
    'CYAN': 'C',
    'MAGENTA': 'M',
    'GRAY': '.',
}

ID = {
    0: ' ',
    1: 'T',
    2: 'R',
    3: 'P',
    4: '?',
    5: '?',
}

class GridWorldRenderer:
    def __init__(self):
        self.grid_world = []

    def render(self, grid_world, left_pane):
        """Renders the grid_world to the left pane in the terminal."""
        self.render_game_state(grid_world, left_pane)

    def render_game_state(self, state, left_pane):
        """Converts grid state into terminal characters and displays it in the left pane."""
        # Clear the left pane before rendering
        left_pane.clear()
        left_pane.border()

        # Render the grid
        for row in range(state.shape[0]):
            for col in range(state.shape[1]):
                cell_value = int(state[row, col])
                # Choose a character to represent the cell's state
                char = ID[cell_value]
                if cell_value == 1:
                    char = ID[cell_value]
                elif cell_value == 2:
                    char = ID[cell_value]
                elif cell_value == 3:
                    char = ID[cell_value]
                
                # Print the character at the correct position in the left pane
                left_pane.addstr(row + 1, col * CELL_SIZE, char * CELL_SIZE)
        
        # Refresh the left pane to update the screen
        left_pane.refresh()

