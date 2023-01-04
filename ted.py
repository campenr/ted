#! python3

import curses
import math

from functools import wraps

def edit(func):
    @wraps(func)
    def wrapper(buffer, stdscr, *args, **kwargs):
        # calculate modified buffer result
        ret = func(buffer, stdscr, *args, **kwargs)
        buffer.x_pos += 1
        # update screen with updated buffer info
        stdscr.deleteln()
        stdscr.insertln()
        y, _ = stdscr.getyx()
        stdscr.move(y, 0)
        stdscr.addstr(buffer.buffer[buffer.buffer_key])
        stdscr.move(y, buffer.x_pos)
        return ret

    return wrapper


class Buffer:

    def __init__(self):
        self.buffer_key = 0
        self.buffer_key_count = 1
        self.buffer = {self.buffer_key: ''}
        self.lines = [self.buffer_key]
        self.x_pos = 0

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

    def move_left(self, stdscr):
        y, x = stdscr.getyx()
        if x > 0:
            self.x_pos -= 1
            stdscr.move(y, self.x_pos)

    def move_right(self, stdscr):
        y, x = stdscr.getyx()
        max_ = len(self.buffer[self.buffer_key])
        if x < max_:
            self.x_pos += 1
            stdscr.move(y, self.x_pos)

    def new_line(self, stdscr):
        # add new empty item to self.buffer/lines state
        self.buffer_key = self.buffer_key_count
        self.buffer[self.buffer_key] = ''
        self.lines.append(self.buffer_key)
        self.buffer_key_count = self.buffer_key_count + 1
        # update cursor
        y, _ = stdscr.getyx()
        self.x_pos = 0
        stdscr.move(y + 1, self.x_pos)

    @edit
    def add_char(self, stdscr, value):
        before = self.buffer[self.buffer_key][0:self.x_pos]
        after = self.buffer[self.buffer_key][self.x_pos:]
        self.buffer[self.buffer_key] = before + value + after

    @edit
    def backspace(self, stdscr):
        self.buffer[self.buffer_key] = self.buffer[self.buffer_key][:-1]


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
        elif key_value == 'KEY_LEFT':
            buffer.move_left(stdscr)
        elif key_value == 'KEY_RIGHT':
            buffer.move_right(stdscr)
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
