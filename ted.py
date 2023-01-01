#! python3

import curses
import math


class Buffer:

    def __init__(self):
        self.buffer_key = 0
        self.buffer_key_count = 1
        self.buffer = {self.buffer_key: ''}
        self.lines = [self.buffer_key]

    def backspace(self, stdscr):
        self.buffer[self.buffer_key] = self.buffer[self.buffer_key][:-1]
        stdscr.deleteln()
        stdscr.insertln()
        y, _ = stdscr.getyx()
        stdscr.move(y, 0)
        stdscr.addstr(self.buffer[self.buffer_key])

    def move_up(self, stdscr):
        index = self.lines.index(self.buffer_key)
        if index > 0:
            self.buffer_key = self.lines[index - 1]
            x = len(self.buffer[self.buffer_key])
            y, _ = stdscr.getyx()
            stdscr.move(y - 1, x)

    def move_down(self, stdscr):
        try:
            index = self.lines.index(self.buffer_key)
            if index < self.buffer_key_count:
                self.buffer_key = self.lines[index + 1]
                x = len(self.buffer[self.buffer_key])
                y, _ = stdscr.getyx()
                stdscr.move(y + 1, x)
        except IndexError:
            pass  # noop

    def new_line(self, stdscr):
        # add new empty item to self.buffer/lines state
        self.buffer_key = self.buffer_key_count
        self.buffer[self.buffer_key] = ''
        self.lines.append(self.buffer_key)
        self.buffer_key_count = self.buffer_key_count + 1
        # update cursor
        y, _ = stdscr.getyx()
        stdscr.move(y + 1, 0)

    def add_char(self, stdscr, value):
        self.buffer[self.buffer_key] += value
        stdscr.deleteln()
        stdscr.insertln()
        y, _ = stdscr.getyx()
        stdscr.move(y, 0)
        stdscr.addstr(self.buffer[self.buffer_key])


##########
# screen #
##########

def _setup_screen(stdscr):

    max_y, max_x = stdscr.getmaxyx()
    title = 'New file'
    padding = ' ' * math.floor((max_x / 2) - (len(title) / 2))
    title_bar = f'{padding}{title}{padding}'
    diff = max_x - len(title_bar)
    title_bar += ' ' * diff

    stdscr.addstr(0, 0, title_bar, curses.A_REVERSE)
    stdscr.refresh()


########
# main #
########

def main():
    curses.wrapper(curses_main)
    return 0


def curses_main(stdscr):

    stdscr.clear()

    _setup_screen(stdscr)
    buffer = Buffer()

    while True:

        stdscr.refresh()

        key_value = stdscr.getkey()

        if key_value == 'KEY_BACKSPACE':
            buffer.backspace(stdscr)
        elif key_value == 'KEY_UP':
            buffer.move_up(stdscr)
        elif key_value == 'KEY_DOWN':
            buffer.move_down(stdscr)
        elif key_value == '\n':
            buffer.new_line(stdscr)
            continue

        else:
            if key_value == 'q':
                break
            else:
                buffer.add_char(stdscr, key_value)


if __name__ == '__main__':
    raise SystemExit(main())
