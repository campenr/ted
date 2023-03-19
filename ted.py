#! python3
import argparse
import curses
import math
from dataclasses import dataclass


class Buffer:

    ORIGINAL = '_original'
    ADD = '_add'

    def __init__(self, initial=''):
        self._original = initial
        self._add = ''
        self._pieces = []

        if initial:
            self._pieces.append(self.Piece(start=0, length=len(initial), source=self.ORIGINAL))

    @dataclass
    class Piece:
        source: str
        start: int
        length: int

    def __str__(self):
        text: str = ''
        for piece in self._pieces:
            source: str = piece.source
            buffer: str = getattr(self, source)
            text += buffer[piece.start:piece.start + piece.length]
        return text

    # to deprecate in favour of insert
    def add_char(self, value):
        self._add += value

    def insert(self, text):
        self._add += text
        self._pieces.append(self.Piece(start=0, length=len(text), source=self.ADD))


class OldBuffer:

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

    def add_char(self, value):
        before = self.buffer[self.buffer_key][0:self.x_pos]
        after = self.buffer[self.buffer_key][self.x_pos:]
        self.buffer[self.buffer_key] = before + value + after
        self.x_pos += 1

    def backspace(self):
        self.buffer[self.buffer_key] = self.buffer[self.buffer_key][:-1]
        self.x_pos += 1


##########
# screen #
##########

NEW_FILE_NAME = '< new file >'


def _write_header(stdscr, filename=None):

    title = filename if filename is not None else NEW_FILE_NAME
    padding = ' ' * math.floor((curses.COLS / 2) - (len(title) / 2))
    header = f'{padding}{title}{padding}'
    diff = curses.COLS - len(header)
    header += ' ' * diff

    stdscr.addstr(0, 0, header, curses.A_REVERSE)


def _write_content(stdscr, buffer):
    lines = str(buffer).splitlines()
    for line_number, line in enumerate(lines, start=1):  # include offset for header.
        if line_number < curses.LINES - 2:  # less one line for the header and footer each.
            stdscr.move(line_number, 0)
            stdscr.addstr(line)


def _write_footer(stdscr):
    status = 'q to quit'
    footer = f"{status}{' ' * (curses.COLS - len(status))}"
    stdscr.insstr(curses.LINES - 1, 0, footer, curses.A_REVERSE)


########
# main #
########

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?')
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
        _write_header(stdscr, filename)
        _write_content(stdscr, buffer)
        _write_footer(stdscr)
        # stdscr.move(buffer.y_pos, buffer.x_pos)
        stdscr.move(1, 0)
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
        elif key_value == 'q':
            with open('outfile', 'w') as f:
                f.write(str(buffer))
            break
        else:
            buffer.add_char(key_value)


if __name__ == '__main__':
    raise SystemExit(main())
