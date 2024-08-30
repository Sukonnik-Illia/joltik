# ruff: noqa
import curses
from threading import Thread

# from queue import Queue
from time import sleep
from curses import KEY_RIGHT as RIGHT, KEY_LEFT as LEFT, KEY_DOWN as DOWN, KEY_UP as UP
from _curses import window


heads = (">", "<", "^", "v")
apple = "@"
speed = 0.2
direction = 0
gameover = False
startlength = 5


def turn_snake(screen: window) -> None:
    global direction
    global gameover
    while True:
        pressed = screen.getch()
        if pressed == RIGHT and direction != 1:
            direction = 0
        elif pressed == LEFT and direction != 0:
            direction = 1
        elif pressed == UP and direction != 3:
            direction = 2
        elif pressed == DOWN and direction != 2:
            direction = 3
        elif pressed == ord("q"):
            gameover = True


def move_snake(direction: int, head: list) -> list:
    if direction == 0:
        head[1] += 1
    elif direction == 1:
        head[1] -= 1
    elif direction == 2:
        head[0] -= 1
    elif direction == 3:
        head[0] += 1
    return head


def gameover_check(head: list, body: list[list], max_y: int, max_x: int) -> bool:
    if head in body or head[0] == max_y or head[0] == 0 or head[1] == max_x or head[1] == 0:
        print("GAME OVER")
        sleep(2)
        return True
    else:
        return False


def main(screen: window) -> None:
    Thread(target=turn_snake, args=[screen], daemon=True).start()
    global direction
    global gameover
    curses.curs_set(0)
    max_y, max_x = screen.getmaxyx()

    # screen borders for clear gameover check
    screen.border()
    # for i in range(max_y):
    #     screen.addch(i, 1, "|")
    #     screen.addch(i, max_x - 2, "|")
    # for j in range(max_x):
    #     screen.addch(1, j, "~")
    #     screen.addch(max_y - 2, j, "~")

    x = int(round(max_x / 2, 0))
    y = int(round(max_y / 2, 0))
    head = [y, x]
    body = [head[:]] * startlength
    blank_cell = body[-1][:]
    while not gameover:
        # if blank_cell not in body:
        #     screen.addch(blank_cell[0], blank_cell[1], " ")

        headchar = heads[direction]
        screen.addch(head[0], head[1], headchar)
        screen.addch(body[1][0], body[1][1], "#")
        head = move_snake(direction, head)

        # update body coords
        blank_cell = body[-1][:]
        for z in range(len(body) - 1, 0, -1):
            body[z] = body[z - 1]
        screen.refresh()
        gameover = gameover_check(head, body, max_y, max_x)
        body[0] = head[:]

        sleep(speed)

    screen.clear()


curses.wrapper(main)

# snake_face = "\N{MONEY-MOUTH FACE}"
# snake_body = "\N{GRINNING FACE WITH SMILING EYES}"
# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()  # react to keys instantly, without requiring the Enter key
# stdscr.keypad(True)
