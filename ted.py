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
        key_value = stdscr.getkey()

        if key_value == 'KEY_BACKSPACE':
            buffer[line_number] = buffer[line_number][:-1]
            # TODO: probably a more efficient thing to do that this.
            stdscr.deleteln()
            stdscr.insertln()
            y, _ = stdscr.getyx()
            stdscr.move(y, 0)
            stdscr.addstr(buffer[line_number])

        elif key_value == '\n':  # TODO: docs say "(unreliable)"
            line_number += 1
            buffer[line_number] = ''  # TODO: need to handle later lines.
            y, _ = stdscr.getyx()
            stdscr.move(y + 1, 0)
            continue

        else:
            if key_value == 'q':
                # teardown curses.
                curses.nocbreak()
                stdscr.keypad(False)
                curses.echo()
                curses.endwin()
                break
            else:
                buffer[line_number] += key_value
                # TODO: probably a more efficient thing to do that this.
                stdscr.deleteln()
                stdscr.insertln()
                y, _ = stdscr.getyx()
                stdscr.move(y, 0)
                stdscr.addstr(buffer[line_number])

        stdscr.refresh()

    print(buffer)


if __name__ == '__main__':
    raise SystemExit(main())
