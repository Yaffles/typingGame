from typingGame import main
import curses
from curses import wrapper
from time import time
import json


def main2(stdscr):
    main(stdscr)


wrapper(main2)
