#! python3

import curses


def main():
    # just accept inputs and then write on exit...

    stdscr = curses.initscr()

    # setup curses. Not we could use curses.wrapper but lets go low level for now to get a handle.
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    stdscr.clear()

    buffer = {0: ''}
    line_number = 0

    while True:
        character = stdscr.getch()

        if character == curses.KEY_BACKSPACE:
            buffer[line_number] = buffer[line_number][:-1]
            curses.filter()
            stdscr.erase()
            stdscr.addstr(buffer[line_number])

        else:
            curses.ungetch(character)
            key_value = stdscr.getkey()

            if key_value == 'q':
                # teardown curses.
                curses.nocbreak()
                stdscr.keypad(False)
                curses.echo()
                curses.endwin()
                break
            else:
                buffer[line_number] += key_value
                curses.filter()
                stdscr.erase()
                stdscr.addstr(buffer[line_number])

        stdscr.refresh()

    print(buffer)


if __name__ == '__main__':
    raise SystemExit(main())
