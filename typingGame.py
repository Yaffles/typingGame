import curses
from curses import wrapper
from time import time, sleep
import json
from random import choice

from _curses import ERR


def init():
    curses.init_pair(1, 2, 0)  # Green
    curses.init_pair(2, 4, 0)  # Red
    curses.init_pair(3, 7, 0)  # White
    curses.init_pair(4, curses.COLOR_CYAN, 0)  # Cyan
    curses.init_pair(5, 9, 0)  # Light Blue
    curses.init_pair(6, 3, 0)  # Aqua
    curses.init_pair(7, 6, 0)  # Yellow
    curses.init_pair(8, curses.COLOR_MAGENTA, 0)  # Magenta


def settings(stdscr):
    with open('typing.json') as myfile:
        options = json.load(myfile)

    stdscr.addstr(0, 0, 'Settings\n', curses.color_pair(7))

    stdscr.addstr('ENTER', curses.color_pair(1))
    stdscr.addstr(' • ', curses.color_pair(2))
    stdscr.addstr('Save changes\n\n', curses.color_pair(6))

    # Mistakes mode
    stdscr.addstr('1', curses.color_pair(1))
    stdscr.addstr(' • ', curses.color_pair(2))
    stdscr.addstr('Mistakes mode', curses.color_pair(6))

    if options['no_mistakes'] == 1:
        stdscr.addstr(3, 25, 'No current mistakes', curses.color_pair(7))
    elif options['no_mistakes'] == 2:
        stdscr.addstr(3, 25, 'Not any mistakes', curses.color_pair(2))
    else:
        stdscr.addstr(3, 25, 'None', curses.color_pair(1))

    # Show mistakes
    stdscr.addstr('\n2', curses.color_pair(1))
    stdscr.addstr(' • ', curses.color_pair(2))
    stdscr.addstr('Show mistakes', curses.color_pair(6))

    if options['show_mistakes'] == 0:
        stdscr.addstr(4, 25, 'Off', curses.color_pair(2))
    else:
        stdscr.addstr(4, 25, 'On', curses.color_pair(1))

    stdscr.addstr('\n3', curses.color_pair(1))
    stdscr.addstr(' • ', curses.color_pair(2))
    stdscr.addstr('Text', curses.color_pair(6))

    if options['text'] == 0:
        stdscr.addstr(5, 25, 'Random', curses.color_pair(2))

    else:
        stdscr.addstr(5, 25, f'{str(options["text"])}     ', curses.color_pair(1))

    done = False

    while True:
        key = stdscr.getch()
        if key in {curses.KEY_ENTER, 10, 13}:
            if done:
                with open('typing.json', 'r+') as k:
                    k.truncate(0)
                    json.dump(options, k)
            return ()
        if key == ord('1'):
            done = True
            if options['no_mistakes'] == 0:
                options['no_mistakes'] = 2
                stdscr.addstr(3, 25, 'Not any mistakes   ', curses.color_pair(2))
            elif options['no_mistakes'] == 1:
                options['no_mistakes'] = False
                stdscr.addstr(3, 25, 'None               ', curses.color_pair(1))
            else:
                options['no_mistakes'] = 1
                stdscr.addstr(3, 25, 'No current mistakes', curses.color_pair(7))

        if key == ord('2'):
            done = True
            if options['show_mistakes'] == 0:
                options['show_mistakes'] = 1
                stdscr.addstr(4, 25, 'On ', curses.color_pair(1))
            else:
                options['show_mistakes'] = 0
                stdscr.addstr(4, 25, 'Off', curses.color_pair(2))

        if key == ord('3'):
            done = True
            if options['text'] == 3:
                options['text'] = 0
                stdscr.addstr(5, 25, 'Random', curses.color_pair(2))
            else:
                options['text'] += 1
                stdscr.addstr(5, 25, f'{str(options["text"])}     ', curses.color_pair(1))


def start(stdscr):
    stdscr.clear()
    stdscr.addstr('Press enter to begin')
    stdscr.addstr('\nPress s to change settings')
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key in {curses.KEY_ENTER, 10, 13}:
            break
        elif key == 115:
            stdscr.clear()
            settings(stdscr)
            stdscr.clear()
            stdscr.addstr('Press enter to begin')
            stdscr.addstr('\nPress s to change settings')
        stdscr.refresh()
    stdscr.clear()


def wpm(stdscr):
    # Show text
    stdscr.refresh()
    # Set variables
    i = 0
    wrong = 0
    current_wrong = 0
    letter_list = []

    # Set options
    with open('typing.json') as options:
        options = json.load(options)
    mistake_mode = options['no_mistakes']
    show_mistakes = options['show_mistakes']
    texts = options["texts"]

    if options["text"]:
        text = texts[options["text"] - 1]
    else:
        text = choice(texts)
    length = len(text)
    stdscr.addstr(text)

    for x in range(length):
        letter_list.append(3)
    correct = 0
    overall_start = time()
    while i < length:
        key = stdscr.getkey()
        height, width = stdscr.getmaxyx()
        stdscr.addstr(6, 0, str(width))
        stdscr.addstr(7, 0, '                          ')
        if str(key) == 'KEY_RESIZE':
            stdscr.addstr(7, 0, 'Resizing may cause crashes', curses.A_BOLD | curses.color_pair(2))
            i -= 1
        elif key == 'KEY_LEFT':
            if i >= 1:
                i -= 2
            else:
                i -= 1
        elif key == 'KEY_RIGHT':
            pass
        elif ord(key) == 8:
            if i >= 1:
                stdscr.addstr(0, i - 1, text[i - 1], curses.color_pair(3))
                letter_list[i - 1] = 3
                i -= 2
            else:
                i -= 1
        elif ord(key) == 27:
            raise SystemExit(0)
        elif key == text[i]:
            letter_list[i] = 0
            stdscr.addstr(0, i, text[i], curses.color_pair(1))
            correct += 1
        else:
            letter_list[i] = 1
            stdscr.addstr(0, i, text[i], curses.color_pair(2))
            wrong += 1
            current_wrong += 1
            if mistake_mode == 2:
                break
        cpm = round(correct / ((time() - overall_start) / 60))
        stdscr.addstr(16, 0, str(i) + ' ', curses.color_pair(3))
        stdscr.addstr(4, 0, str(cpm) + ' cpm  ', curses.color_pair(3))
        i += 1
        current_wrong = letter_list.count(1)
        if show_mistakes == 1:
            for f in range(len(letter_list)):
                if length <= width:
                    stdscr.addstr(5, 0, "                                ")
                    if letter_list[f] == 1:
                        stdscr.addstr(1, f, '▲', curses.color_pair(6))
                        stdscr.addstr(2, f, '│', curses.color_pair(6))
                    else:
                        stdscr.addstr(1, f, ' ')
                        stdscr.addstr(2, f, ' ')
                else:
                    stdscr.addstr(5, 0, "Increase window width and reload", curses.A_STANDOUT)
        if i > 0:
            stdscr.move(0, i)
        else:
            stdscr.move(0, 0)

        if mistake_mode:
            if length == i and current_wrong > 0 and mistake_mode == 1:
                stdscr.addstr(7, 0, f'There is {current_wrong} mistakes that must be fixed', curses.color_pair(2))
        elif length == i:
            break
        stdscr.refresh()

    right = round(((length - wrong) / length) * 100, 2)
    if wrong == 0:
        stdscr.addstr(5, 0, 'No wrong letters', curses.color_pair(3))
    elif wrong == 1:
        stdscr.addstr(5, 0, '1 wrong letter', curses.color_pair(3))
    else:
        stdscr.addstr(5, 0, str(wrong) + ' wrong letters', curses.color_pair(3))
    stdscr.addstr(6, 0, str(right) + '%', curses.color_pair(1))
    if mistake_mode == 2 and wrong > 0:
        stdscr.addstr(7, 0, f'There is {current_wrong} mistakes\nYou failed', curses.color_pair(2))
    else:
        stdscr.addstr(7, 0, '                                                           ', curses.color_pair(2))
    stdscr.getkey()
    sleep(1.5)
    stdscr.refresh()


def main(stdscr):
    init()
    while True:
        start(stdscr)
        wpm(stdscr)


wrapper(main)
