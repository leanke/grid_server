import curses
import random
import time
import numpy as np
import curses.textpad
import threading  # Add threading import
import curses.textpad  # Add textpad import

screen_print = {

    'tbu11': '▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟',
    'tbu12': '□▢▣▤▥▦▧▨▩▪▫▬▭▮▯',
    'tbu13': '▰▱▲△▴▵▶▷▸▹►▻▼▽▾▿',
    'tbu14': '◀◁◂◃◄◅◆◇◈◉◊○◌◍◎',
    'tbu15': '●◐◑◒◓◔◕◖◗◘◙◚◛◜◝◞◟',
    'tbu16': '◠◡◢◣◤◥◦◧◨◩◪◫◬◭◮◯',
    'tbu17': '◰◱◲◳◴◵◶◷◸◹◺◻◼◽◾◿',
}

class Inventory:
    def __init__(self):
        self.inventory = {}
        self.equipped = {
            'head': None,
            'body': None,
            'legs': None,
        }
        self.text_queue = []

    def add_item(self, item, quantity):
        if item not in self.inventory:
            self.inventory[item] = quantity
        else:
            self.inventory[item] += quantity
    
    def remove_item(self, item, quantity):
        if item in self.inventory:
            self.inventory[item] -= quantity
            if self.inventory[item] <= 0:
                del self.inventory[item]

    def get_inventory(self):
        return self.inventory
    
    def equip_item(self, item):
        if item.slot in self.equipped:
            if self.equipped[item.slot] is None:
                self.equipped[item.slot] = item
            else:
                self.text_queue.append('Slot already occupied')
    
    def unequip_item(self, item):
        if item.slot in self.equipped:
            if self.equipped[item.slot] is not None:
                self.equipped[item.slot] = None
            else:
                self.text_queue.append('Slot already empty')
        
class Item:
    def __init__(self, name, description, slot):
        self.name = name
        self.description = description
        self.slot = slot

    @staticmethod
    def create_item(name, description, slot):
        return Item(name, description, slot)

class Test:
    def __init__(self):
        self.items = {
            1: Item.create_item('Head', 'A head', 'head'),
            2: Item.create_item('Body', 'A body', 'body'),
            3: Item.create_item('Legs', 'A pair of legs', 'legs'),
        }
        self.inventory = Inventory()
        self.screen_array = np.zeros(2)
        self.screen_panel = None
        self.menu_right_panel = None
        self.menu_left_panel = None
        self.text_panel = None
        self.stdscr = None
        self.login_array = None
        self.username = None
        self.password = None
        # Text panel
        self.text_queue = []
        self.text_toggle = 0
        self.counter = 0

    def resize(self, stdscr):
        height, width = stdscr.getmaxyx()
        screen_width = width // 2
        qwidth = width // 4
        text_height = height // 2

        self.screen_panel = curses.newwin(height, screen_width, 0, 0)
        self.menu_right_panel = curses.newwin(text_height, qwidth, 0, screen_width + qwidth)
        self.menu_left_panel = curses.newwin(text_height, qwidth, 0, screen_width)
        self.text_panel = curses.newwin(text_height, screen_width, text_height, screen_width)

    def init_colors(self):
        curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(13, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(14, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(15, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(16, curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(17, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(18, curses.COLOR_MAGENTA, curses.COLOR_WHITE)

        curses.init_pair(21, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(22, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(23, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(24, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(25, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(26, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(27, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(28, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        curses.init_pair(31, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(32, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(33, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(34, curses.COLOR_BLUE, curses.COLOR_GREEN)
        curses.init_pair(35, curses.COLOR_RED, curses.COLOR_GREEN)
        curses.init_pair(36, curses.COLOR_YELLOW, curses.COLOR_GREEN)
        curses.init_pair(37, curses.COLOR_CYAN, curses.COLOR_GREEN)
        curses.init_pair(38, curses.COLOR_MAGENTA, curses.COLOR_GREEN)

        curses.init_pair(41, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(42, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(43, curses.COLOR_GREEN, curses.COLOR_BLUE)
        curses.init_pair(44, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(45, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(46, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.init_pair(47, curses.COLOR_CYAN, curses.COLOR_BLUE)
        curses.init_pair(48, curses.COLOR_MAGENTA, curses.COLOR_BLUE)

        curses.init_pair(51, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(52, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(53, curses.COLOR_GREEN, curses.COLOR_RED)
        curses.init_pair(54, curses.COLOR_BLUE, curses.COLOR_RED)
        curses.init_pair(55, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(56, curses.COLOR_YELLOW, curses.COLOR_RED)
        curses.init_pair(57, curses.COLOR_CYAN, curses.COLOR_RED)
        curses.init_pair(58, curses.COLOR_MAGENTA, curses.COLOR_RED)

        curses.init_pair(61, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(62, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(63, curses.COLOR_GREEN, curses.COLOR_YELLOW)
        curses.init_pair(64, curses.COLOR_BLUE, curses.COLOR_YELLOW)
        curses.init_pair(65, curses.COLOR_RED, curses.COLOR_YELLOW)
        curses.init_pair(66, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        curses.init_pair(67, curses.COLOR_CYAN, curses.COLOR_YELLOW)
        curses.init_pair(68, curses.COLOR_MAGENTA, curses.COLOR_YELLOW)

        curses.init_pair(71, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(72, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(73, curses.COLOR_GREEN, curses.COLOR_CYAN)
        curses.init_pair(74, curses.COLOR_BLUE, curses.COLOR_CYAN)
        curses.init_pair(75, curses.COLOR_RED, curses.COLOR_CYAN)
        curses.init_pair(76, curses.COLOR_YELLOW, curses.COLOR_CYAN)
        curses.init_pair(77, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(78, curses.COLOR_MAGENTA, curses.COLOR_CYAN)

        curses.init_pair(81, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        curses.init_pair(82, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(83, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
        curses.init_pair(84, curses.COLOR_BLUE, curses.COLOR_MAGENTA)
        curses.init_pair(85, curses.COLOR_RED, curses.COLOR_MAGENTA)
        curses.init_pair(86, curses.COLOR_YELLOW, curses.COLOR_MAGENTA)
        curses.init_pair(87, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
        curses.init_pair(88, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)


    def text(self, text):
        y, x = self.text_panel.getmaxyx()
        max_lines = y - 2
        self.text_queue.append(text)
        if len(self.text_queue) > max_lines:
            diff = len(self.text_queue) - max_lines
            self.text_queue = self.text_queue[diff:]
        self.text_panel.box()
        for i, text in enumerate(self.text_queue):
            self.text_panel.addstr(i+1, 1, text + ' ' * ((x - 2) - len(text)))
        # self.text_panel.addstr(0, 0, text)
        self.text_panel.refresh()
    
    def menu_left(self):
        self.menu_left_panel.box()
        y, x = self.menu_left_panel.getmaxyx()
        for i, slot in enumerate(self.inventory.get_inventory().keys()):
            text = f'{slot}: {self.inventory.get_inventory()[slot]}'
            self.menu_left_panel.addstr(i+1, 1, text + ' ' * ((x - 2) - len(text)))
        self.menu_left_panel.refresh()

    def menu_right(self, username, password):
        self.menu_right_panel.box()
        y, x = self.menu_right_panel.getmaxyx()
        user = f"Username: {username} Password: {password}"
        self.menu_right_panel.addstr(2, 1, user + ' ' * ((x - 2) - len(user)))
        for i, slot in enumerate(self.inventory.equipped.keys()):
            line = i + 2
            if self.inventory.equipped[slot] is not None:
                text = f"{slot}: {self.inventory.equipped[slot].name}"
            else:
                text = f"{slot}: {self.inventory.equipped[slot]}"
            self.menu_right_panel.addstr(line, 1, text + ' ' * ((x - 2) - len(text)))
        self.menu_right_panel.refresh()
    
    def screen(self):
        my, mx = self.screen_panel.getmaxyx()
        self.screen_array = np.zeros((my-1, mx-1))
        if self.counter % 2 == 0:
            for i in range(self.screen_array.shape[0]):
                for j in range(self.screen_array.shape[1]):
                    self.screen_array[i, j] = 2
                    if i % 2 == 0:
                        self.screen_array[i, j] = 3
                    if j % 2 == 0:
                        self.screen_array[i, j] = 3
        else:
            for i in range(self.screen_array.shape[0]):
                for j in range(self.screen_array.shape[1]):
                    self.screen_array[i, j] = 3
                    if i % 2 == 0:
                        self.screen_array[i, j] = 2
                    if j % 2 == 0:
                        self.screen_array[i, j] = 2
        for x in range(self.screen_array.shape[0]):
            for y in range(self.screen_array.shape[1]):
                if self.screen_array[x, y] == 1:
                    self.screen_panel.addstr(x, y, ' ', curses.color_pair(11))
                elif self.screen_array[x, y] == 2:
                    self.screen_panel.addstr(x, y, ' ', curses.color_pair(31))
                elif self.screen_array[x, y] == 3:
                    self.screen_panel.addstr(x, y, ' ', curses.color_pair(41))
                elif self.screen_array[x, y] == 4:
                    self.screen_panel.addstr(x, y, ' ', curses.color_pair(51))
                else:
                    self.screen_panel.addstr(x, y, ' ', curses.color_pair(11))

        self.screen_panel.refresh()

    def update(self, username, password):
        self.screen()
        if self.text_toggle == 0:
            self.text('First')
            self.text_toggle = 1
        elif self.text_toggle == 1:
            self.text('Second')
            self.text_toggle = 2
        elif self.text_toggle == 2:
            self.text('Third')
            self.text_toggle = 3
        elif self.text_toggle == 3:
            self.counter += 1
            self.text(f'Counter: {self.counter}')
            self.text_toggle = 0
        self.menu_left()
        self.menu_right(username, password)


    def handle_input(self, stdscr, username, password):
        stdscr.nodelay(True)
        stdscr.timeout(100)  # Add this line to set a timeout for getch
        y, x = stdscr.getmaxyx()
        self.update(username, password)
        # resize = curses.is_term_resized(y, x)

        while True:
            resize = curses.is_term_resized(y, x)
            if resize is True:
                y, x = stdscr.getmaxyx()
                stdscr.clear()
                curses.resizeterm(y, x)
                self.resize(stdscr)
                stdscr.refresh()
            command = stdscr.getch()
            if command == -1:
                continue
            elif chr(command) == '1':
                if self.inventory:
                    self.inventory.add_item(1, 1)
                else:
                    self.text_queue.append('Inventory full')
            elif chr(command) == '2':
                if self.inventory:
                    self.inventory.add_item(2, 1)
                else:
                    self.text_queue.append('Inventory full')
            elif chr(command) == '3':
                if self.inventory:
                    self.inventory.add_item(3, 1)
                else:
                    self.text_queue.append('Inventory full')
            elif chr(command) == 'f':
                self.update(username, password)
            elif chr(command) == 'e':
                self.inventory.equip_item(self.items[1])
            elif chr(command) == 'r':
                self.inventory.unequip_item(self.items[1])
            if chr(command) == 'q':
                self.close()
                break

    def login_animation(self, stdscr, screen_hight, screen_width, ch, cw, center):
        # while idle:
        for x in range(self.login_array.shape[0]):
            for y in range(self.login_array.shape[1]):
                # Exclude writing in the center coordinates
                if screen_hight <= x < screen_hight + ch and screen_width <= y < screen_width + cw:
                    continue
                self.login_array[x, y] = random.choice([1, 2, 3])
                if self.login_array[x, y] == 1:
                    stdscr.addstr(x, y, ' ', curses.color_pair(21))
                elif self.login_array[x, y] == 2:
                    stdscr.addstr(x, y, ' ', curses.color_pair(31))
                elif self.login_array[x, y] == 3:
                    stdscr.addstr(x, y, ' ', curses.color_pair(41))
                else:
                    stdscr.addstr(x, y, ' ', curses.color_pair(21))
        stdscr.refresh()
        center.box()
        center.addstr(1, (cw-6)//2, f'Log in')
        center.addstr(4, 1, 'Username: ')
        center.addstr(6, 1, 'Password: ')
        center.refresh()
        # time.sleep(0.5)



    def login(self, stdscr):
        height, width = stdscr.getmaxyx()
        screen_width = width // 3
        screen_hight = height // 3
        if self.login_array is None:
            self.login_array = np.full((height-1, width-1), random.choice([1, 2, 3]))
        center = curses.newwin(screen_hight, screen_width, screen_hight, screen_width)
        ch, cw = center.getmaxyx()
        username_win = curses.newwin(1, cw - 12, screen_hight + 4, screen_width + 11)
        password_win = curses.newwin(1, cw - 12, screen_hight + 6, screen_width + 11)
        username_box = curses.textpad.Textbox(username_win)
        password_box = curses.textpad.Textbox(password_win)

        # idle = True
        # if self.username is not None and self.password is not None:
        #     idle = False

        self.login_animation(stdscr, screen_hight, screen_width, ch, cw, center)


        curses.echo() 
        curses.nocbreak()
        self.username = username_box.edit()
        username_win.refresh()
        self.password = password_box.edit()
        password_win.refresh()
        curses.cbreak()
        curses.noecho()

        return self.username, self.password



    def main(self, stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

        self.stdscr = stdscr
        self.init_colors()
        username, password = self.login(stdscr)
        self.resize(stdscr)
        self.handle_input(stdscr, username, password)
    
    def close(self):
        curses.endwin()



class ButtonHandler:
    def __init__(self):
        self.buttons = {
            'a': 'reassign',
            'b': False,
            'c': False,
            'd': False,
        }

    def handle_input(self, stdscr):
        stdscr.nodelay(True)
        stdscr.timeout(100)

if __name__ == '__main__':
    test = Test()
    curses.wrapper(test.main)
