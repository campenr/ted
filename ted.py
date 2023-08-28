#! python3
import argparse
import curses
import math
from dataclasses import dataclass


@dataclass
class Piece:
    source: str
    start: int
    length: int


class Buffer:

    ORIGINAL = '_original'
    ADD = '_add'

    def __init__(self, initial=''):
        self._original = initial
        self._add = ''
        self._piece_table = []

        if initial:
            self._piece_table.append(Piece(start=0, length=len(initial), source=self.ORIGINAL))

    def __str__(self):
        text: str = ''
        for piece in self._piece_table:
            source: str = piece.source
            buffer: str = getattr(self, source)
            text += buffer[piece.start:piece.start + piece.length]
        return text

    def __len__(self):
        return len(str(self))

    # to deprecate in favour of insert
    def add_char(self, value):
        self._add += value

    def insert(self, text, index):

        # shortcut handling of the special cases of the first add, or an addition at index 0 to avoid work.
        # if index == 0 or len(self._add) == 0:
        if index == 0:
            piece = Piece(start=len(self._add), length=len(text), source=self.ADD)
            self._piece_table.insert(0, piece)

        else:
            table_index, piece_index = self._get_indexes(index)

            if table_index is None:
                # no matching piece, so we need to add one at the end. special case for the first addition
                # when it is at the end.
                piece = Piece(start=len(self._add), length=len(text), source=self.ADD)
                self._piece_table.append(piece)

            else:
                old_piece = self._piece_table[table_index]
                left, right = self._split_piece(old_piece, piece_index)

                if left.source == self.ORIGINAL:
                    # we can't append original pieces, so we need to create an add piece.
                    piece = Piece(start=len(self._add), length=len(text), source=self.ADD)
                    new = [left, piece, right]
                    self._piece_table = self._piece_table[0:table_index] + new + self._piece_table[table_index + 1:]
                elif piece_index == old_piece.length:
                    old_piece.length += len(text)
                else:
                    piece = Piece(start=old_piece.length, length=len(text), source=self.ADD)
                    new = [left, piece, right]
                    self._piece_table = self._piece_table[0:table_index] + new + self._piece_table[table_index + 1:]

        self._add += text

    def _get_indexes(self, char_index):
        accumulator = 0
        for table_index, piece in enumerate(self._piece_table):
            accumulator += piece.length
            if char_index <= accumulator:
                piece_index = piece.length - (accumulator - char_index)
                return table_index, piece_index
        return None, None

    @staticmethod
    def _split_piece(piece, index):
        return [
            Piece(start=piece.start, length=index, source=piece.source),
            Piece(start=index, length=piece.length - index, source=piece.source),
        ]


@dataclass
class FilePosition:
    x: int
    y: int


class File:

    def __init__(self, buffer: Buffer, file_position: FilePosition) -> None:
        self._buffer = buffer
        self._file_position = file_position

    @property
    def char_pos(self) -> int:
        return self._file_position.x

    @char_pos.setter
    def char_pos(self, value: int) -> None:
        self._file_position.x = value

    @property
    def line_pos(self) -> int:
        return self._file_position.y

    @line_pos.setter
    def line_pos(self, value: int) -> None:
        self._file_position.y = value

    def move_left(self):
        if self.char_pos > 0:
            self.char_pos -= 1

    def move_right(self):
        if self.char_pos < len(self._buffer):
            self.char_pos += 1

    def move_down(self):
        lines = 0
        for char in str(self._buffer):
            if char == '\n':
                lines += 1

        if self.line_pos < lines:
            self.line_pos += 1

    def move_up(self):
        if self.line_pos > 0:
            self.line_pos -= 1


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
            buffer = Buffer(f.read())
    else:
        buffer = Buffer()

    file = File(buffer)
    header_offset = 1

    while True:

        # draw
        stdscr.clear()
        _write_header(stdscr, filename)
        _write_content(stdscr, buffer)
        _write_footer(stdscr)
        stdscr.move(file.line_pos + header_offset, file.char_pos)
        stdscr.refresh()

        key_value = stdscr.getkey()

        if key_value == 'KEY_LEFT':
            file.move_left()
        elif key_value == 'KEY_RIGHT':
            file.move_right()
        elif key_value == 'q':
            with open('outfile', 'w') as f:
                f.write(str(buffer))
            break
        else:
            file.move_right()
            buffer.insert(key_value, file.line_pos + header_offset * file.char_pos)


if __name__ == '__main__':
    raise SystemExit(main())
