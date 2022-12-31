#! python3

import curses
import math


###########
# actions #
###########

def backspace(stdscr, buffer, buffer_key, buffer_key_count, lines):
    buffer[buffer_key] = buffer[buffer_key][:-1]
    # TODO: probably a more efficient thing to do that this.
    stdscr.deleteln()
    stdscr.insertln()
    y, _ = stdscr.getyx()
    stdscr.move(y, 0)
    stdscr.addstr(buffer[buffer_key])

    return buffer, buffer_key, buffer_key_count, lines


def move_up(stdscr, buffer, buffer_key, buffer_key_count, lines):
    index = lines.index(buffer_key)
    if index > 0:
        buffer_key = lines[index - 1]
        x = len(buffer[buffer_key])
        y, _ = stdscr.getyx()
        stdscr.move(y - 1, x)

    return buffer, buffer_key, buffer_key_count, lines


def move_down(stdscr, buffer, buffer_key, buffer_key_count, lines):
    try:
        index = lines.index(buffer_key)
        if index < buffer_key_count:
            buffer_key = lines[index + 1]
            x = len(buffer[buffer_key])
            y, _ = stdscr.getyx()
            stdscr.move(y + 1, x)
    except IndexError:
        pass  # noop

    return buffer, buffer_key, buffer_key_count, lines


def new_line(stdscr, buffer, buffer_key, buffer_key_count, lines):
    # add new empty item to buffer/lines state
    buffer_key = buffer_key_count
    buffer[buffer_key] = ''
    lines.append(buffer_key)
    buffer_key_count = buffer_key_count + 1
    # update cursor
    y, _ = stdscr.getyx()
    stdscr.move(y + 1, 0)

    return buffer, buffer_key, buffer_key_count, lines


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
    res = curses.wrapper(curses_main)
    print(res)
    return 0


def curses_main(stdscr):

    stdscr.clear()

    _setup_screen(stdscr)

    buffer_key = 0
    buffer_key_count = 1
    buffer = {buffer_key: ''}
    lines = [buffer_key]

    while True:

        stdscr.refresh()

        key_value = stdscr.getkey()

        if key_value == 'KEY_BACKSPACE':
            buffer, buffer_key, buffer_key_count, lines = backspace(stdscr, buffer, buffer_key, buffer_key_count, lines)
        elif key_value == 'KEY_UP':
            buffer, buffer_key, buffer_key_count, lines = move_up(stdscr, buffer, buffer_key, buffer_key_count, lines)
        elif key_value == 'KEY_DOWN':
            buffer, buffer_key, buffer_key_count, lines = move_down(stdscr, buffer, buffer_key, buffer_key_count, lines)
        elif key_value == '\n':
            buffer, buffer_key, buffer_key_count, lines = new_line(stdscr, buffer, buffer_key, buffer_key_count, lines)
            continue

        else:
            if key_value == 'q':
                break
            else:
                buffer[buffer_key] += key_value
                # TODO: probably a more efficient thing to do that this.
                stdscr.deleteln()
                stdscr.insertln()
                y, _ = stdscr.getyx()
                stdscr.move(y, 0)
                stdscr.addstr(buffer[buffer_key])

    return buffer, lines


if __name__ == '__main__':
    raise SystemExit(main())
