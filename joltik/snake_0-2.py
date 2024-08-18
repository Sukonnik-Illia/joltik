# ruff: noqa
import curses
import random
from threading import Thread
from time import sleep
from curses import KEY_RIGHT as RIGHT, KEY_LEFT as LEFT, KEY_DOWN as DOWN, KEY_UP as UP
from _curses import window


class Field:
    def __init__(self, screen: window):
        self.max_y, self.max_x = screen.getmaxyx()
        self.start_position = [self.max_y // 2, self.max_x // 2]


class Apple(Field):
    def __init__(self, field: Field):
        self.apples = "@"

    def spawn_apple(self, screen: window, field: Field, snakebody: list[list]):
        snake_y = [y[0] for y in snakebody]
        snake_x = [x[0] for x in snakebody]
        apple_y = random.choice([i for i in range(1, field.max_y - 1) if i not in snake_y])
        apple_x = random.choice([i for i in range(1, field.max_x - 1) if i not in snake_x])
        self.apple = [apple_y, apple_x]
        return self.apple


class Snake(Field):
    def __init__(self, field: Field, start_len=5):
        self.direction = 0
        self.head = field.start_position[:]  # start position from class Field
        self.body = [self.head[:]] * start_len  # firther to make len dinamyc
        self.heads = (">", "<", "^", "v")
        self.quit = False

    def feed_snake(self):
        self.body.append(self.body[len(self.body) - 1])

    def move_snake(self, screen: window):
        headchar = self.heads[self.direction]
        for i in range(len(self.body)):
            screen.addch(self.body[i][0], self.body[i][1], "#")
        screen.addch(self.head[0], self.head[1], headchar)
        if self.direction == 0:
            self.head[1] += 1
        elif self.direction == 1:
            self.head[1] -= 1
        elif self.direction == 2:
            self.head[0] -= 1
        elif self.direction == 3:
            self.head[0] += 1

        # update body coords
        for z in range(len(self.body) - 1, 0, -1):
            self.body[z] = self.body[z - 1]
        self.body[0] = self.head[:]

        return self.head, self.body

    def check_collision(self, field: Field):
        # Check for collisions with the body or borders
        if (
            self.head in self.body[1:]
            or self.head[0] == 0
            or self.head[0] == field.max_y
            or self.head[1] == 0
            or self.head[1] == field.max_x - 1
        ):
            return True
        return False

    def change_direction(self, new_direction) -> None:
        if new_direction == RIGHT and self.direction != 1:
            self.direction = 0
        elif new_direction == LEFT and self.direction != 0:
            self.direction = 1
        elif new_direction == UP and self.direction != 3:
            self.direction = 2
        elif new_direction == DOWN and self.direction != 2:
            self.direction = 3

    def turn_snake(self, screen: window):
        while True:
            pressed = screen.getch()
            if pressed in (RIGHT, LEFT, UP, DOWN):
                self.change_direction(pressed)
                sleep(0.1)
            elif pressed == ord("q"):
                self.quit = True
                print("Quitting the game")
                return self.quit


class Game(Snake):
    def __init__(self, screen: window):
        self.screen = screen
        self.speed = 0.3
        self.gameover = False
        self.applespawn = False

    def setup(self):
        curses.curs_set(0)
        self.field = Field(self.screen)
        self.snake = Snake(self.field)
        self.apple = Apple(self.field)

    def run(self):
        self.setup()

        Thread(target=self.snake.turn_snake, args=[self.screen], daemon=True).start()

        while not self.gameover:
            self.screen.clear()
            self.screen.border()
            self.snake.move_snake(self.screen)
            self.gameover = self.snake.check_collision(self.field)
            if self.snake.quit == True:
                self.gameover = True
                sleep(1)
            if not self.applespawn:
                new_apple = self.apple.spawn_apple(
                    screen=self.screen, field=self.field, snakebody=self.snake.body
                )
                self.applespawn = True
            if self.snake.head == new_apple:
                self.screen.addch(new_apple[0], new_apple[1], " ")
                self.snake.feed_snake()
                self.applespawn = False
            self.screen.addch(new_apple[0], new_apple[1], self.apple.apples)
            self.screen.refresh()
            sleep(self.speed)
        self.screen.clear()
        self.screen.addstr(self.field.max_y // 2, self.field.max_x // 2 - 5, "GAME OVER")
        self.screen.refresh()
        sleep(2)


def main(screen: window):
    game = Game(screen)
    game.run()


curses.wrapper(main)


# class Snake_gpt:
#     def __init__(self, start_pos, start_length=5):
#         self.direction = 0  # Start moving right
#         self.body = [start_pos[:] for _ in range(start_length)]
#         self.head = self.body[0]
#         self.heads = (">", "<", "^", "v")

#     def move(self):
#         if self.direction == 0:
#             self.head[1] += 1
#         elif self.direction == 1:
#             self.head[1] -= 1
#         elif self.direction == 2:
#             self.head[0] -= 1
#         elif self.direction == 3:
#             self.head[0] += 1

#         # Update body
#         blank_cell = self.body[-1][:]
#         for z in range(len(self.body) - 1, 0, -1):
#             self.body[z] = self.body[z - 1]
#         self.body[0] = self.head[:]

#         return blank_cell

#     def change_direction(self, new_direction):
#         # Prevent the snake from reversing
#         if (
#             new_direction == RIGHT
#             and self.direction != 1
#             or new_direction == LEFT
#             and self.direction != 0
#             or new_direction == UP
#             and self.direction != 3
#             or new_direction == DOWN
#             and self.direction != 2
#         ):
#             self.direction = new_direction

#     def check_collision(self, max_y, max_x):
#         # Check for collisions with the body or borders
#         if (
#             self.head in self.body[1:]
#             or self.head[0] == 0
#             or self.head[0] == max_y - 1
#             or self.head[1] == 0
#             or self.head[1] == max_x - 1
#         ):
#             return True
#         return False

#     def draw(self, screen):
#         head_char = self.heads[self.direction]
#         screen.addch(self.head[0], self.head[1], head_char)
#         for segment in self.body[1:]:
#             screen.addch(segment[0], segment[1], "#")


# class Game_gpt:
#     def __init__(self, screen: window):
#         self.screen = screen
#         self.snake = None
#         self.max_y, self.max_x = screen.getmaxyx()
#         self.gameover = False
#         self.speed = 0.2

#     def setup(self):
#         curses.curs_set(0)
#         self.screen.border()
#         x = self.max_x // 2
#         y = self.max_y // 2
#         self.snake = Snake_gpt([y, x])

#     def run(self):
#         self.setup()
#         Thread(target=self.turn_snake, daemon=True).start()
#         while not self.gameover:
#             blank_cell = self.snake.move()
#             if blank_cell not in self.snake.body:
#                 self.screen.addch(blank_cell[0], blank_cell[1], " ")

#             self.snake.draw(self.screen)
#             self.screen.refresh()
#             self.gameover = self.snake.check_collision(self.max_y, self.max_x)
#             sleep(self.speed)

#         self.screen.clear()
#         self.screen.addstr(self.max_y // 2, self.max_x // 2 - 5, "GAME OVER")
#         self.screen.refresh()
#         sleep(2)

#     def turn_snake(self):
#         while not self.gameover:
#             pressed = self.screen.getch()
#             if pressed in (RIGHT, LEFT, UP, DOWN):
#                 self.snake.change_direction(pressed)
#             elif pressed == ord("q"):
#                 self.gameover = True


# def main(screen: window):
#     game = Game_gpt(screen)
#     game.run()


# curses.wrapper(main)
