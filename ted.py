#! python3
import argparse
import curses
import math

from functools import wraps


def edit(func):
    @wraps(func)
    def wrapper(buffer, *args, **kwargs):
        # calculate modified buffer result
        ret = func(buffer, *args, **kwargs)
        return ret

    return wrapper


class Buffer:

    def __init__(self, lines=None):
        self.buffer_key = 0
        self.buffer_key_count = 1
        if lines is not None:
            self.buffer = {}
            self.lines = []
            for line in lines:
                self.buffer[self.buffer_key] = line
                self.lines.append(self.buffer_key)
                self.buffer_key += 1
                self.buffer_key_count += 1
            # reset buffer_key for running the main app
            self.buffer_key = self.lines[0]
        else:
            self.buffer = {self.buffer_key: ''}
            self.lines = [self.buffer_key]
        self.x_pos, self.y_pos = 0, 1  # absolute, accounting for header.

    def move_up(self):
        current_line = self.lines.index(self.buffer_key)
        if current_line > 0:
            self.buffer_key = self.lines[current_line - 1]
            line_length = len(self.buffer[self.buffer_key])
            self.x_pos = line_length if self.x_pos > line_length else self.x_pos
            self.y_pos -= 1

    def move_down(self):
        current_line = self.lines.index(self.buffer_key)
        if current_line < self.buffer_key_count - 1:
            self.buffer_key = self.lines[current_line + 1]
            line_length = len(self.buffer[self.buffer_key])
            self.x_pos = line_length if self.x_pos > line_length else self.x_pos
            self.y_pos += 1

    def move_left(self):
        if self.x_pos > 0:
            self.x_pos -= 1

    def move_right(self):
        line_length = len(self.buffer[self.buffer_key])
        if self.x_pos < line_length:
            self.x_pos += 1

    def new_line(self):
        # add new empty item to self.buffer/lines state
        self.buffer_key = self.buffer_key_count
        self.buffer[self.buffer_key] = ''
        self.lines.append(self.buffer_key)
        self.buffer_key_count += 1
        # update cursor
        self.x_pos = 0
        self.y_pos += 1

    @edit
    def add_char(self, value):
        before = self.buffer[self.buffer_key][0:self.x_pos]
        after = self.buffer[self.buffer_key][self.x_pos:]
        self.buffer[self.buffer_key] = before + value + after
        self.x_pos += 1

    @edit
    def backspace(self):
        self.buffer[self.buffer_key] = self.buffer[self.buffer_key][:-1]
        self.x_pos += 1


##########
# screen #
##########

def _write_header(stdscr):

    max_y, max_x = stdscr.getmaxyx()
    title = 'New file'
    padding = ' ' * math.floor((max_x / 2) - (len(title) / 2))
    title_bar = f'{padding}{title}{padding}'
    diff = max_x - len(title_bar)
    title_bar += ' ' * diff

    stdscr.addstr(0, 0, title_bar, curses.A_REVERSE)


########
# main #
########

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    curses.wrapper(curses_main, args.filename)
    return 0


def curses_main(stdscr, filename=None):

    if filename is not None:
        with open(filename) as f:
            buffer = Buffer(f.readlines())
    else:
        buffer = Buffer()

    while True:

        # draw
        stdscr.clear()
        _write_header(stdscr)
        for line_number, line_key in enumerate(buffer.lines, start=1):  # include offset for header.
            if line_number < curses.LINES - 2:
                stdscr.move(line_number, 0)
                stdscr.addstr(buffer.buffer[line_key])
        stdscr.move(buffer.y_pos, buffer.x_pos)
        stdscr.refresh()

        key_value = stdscr.getkey()
        if key_value == 'KEY_BACKSPACE':
            buffer.backspace()
        elif key_value == 'KEY_UP':
            buffer.move_up()
        elif key_value == 'KEY_DOWN':
            buffer.move_down()
        elif key_value == 'KEY_LEFT':
            buffer.move_left()
        elif key_value == 'KEY_RIGHT':
            buffer.move_right()
        elif key_value == '\n':
            buffer.new_line()
            continue

        else:
            if key_value == 'q':
                with open('outfile', 'w') as f:
                    f.write('\n'.join(buffer.buffer.values()))
                break
            else:
                buffer.add_char(key_value)


if __name__ == '__main__':
    raise SystemExit(main())
