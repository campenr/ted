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

    buffer = []

    while True:
        input_ = stdscr.getkey()

        if input_ == 'q':
            # teardown curses.
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            break

        stdscr.addch(input_)

        buffer.append(input_)

        stdscr.refresh()

    print(buffer)


if __name__ == '__main__':
    raise SystemExit(main())
