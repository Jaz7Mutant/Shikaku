from copy import copy, deepcopy
from time import sleep

import math
from pyglet.window import key, mouse

from Solver.game_board import GameBoard
from Utilities.point import Point
from Utilities.texture_colors import COLORS
from Utilities.texture_factory import TextureFactory
from Utilities.rectangle import Rectangle
from pyglet.gl import *


class Game(pyglet.window.Window):
    def __init__(self, filename, game_board: GameBoard, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        self.filename = filename
        self.pressed_cords = []
        self.released_cords = []
        self.game_board = game_board
        self.parent = parent
        self.game_board.initialize_board_solution()
        self.squares_backup = [game_board.cols * [0] for i in range(game_board.rows)]
        self.solution_backup = game_board.solution.copy()
        self.squares = [game_board.cols * [Square] for i in range(game_board.rows)]
        # self.square_size = 20
        self.square_size = self.height // (game_board.cols + 1)
        self.start_x = self.square_size//2
        self.start_y = self.square_size//2
        n = 0
        for y, row in enumerate(game_board.board):
            # self.squares.append(list())
            for x, symbol in enumerate(row):
                rev_y = game_board.cols - y - 1
                color = (180, 210, 230)
                num = ' '
                if symbol == -1:
                    num = ' '
                else:
                    game_board.solution[y][x] = n
                    n += 1
                    num = str(symbol)
                    color = copy(COLORS[int(game_board.solution[y][x]) % (len(COLORS) - 1)][0:3])
                self.squares[rev_y][x] = (
                    Square(
                        num,
                        Point(
                            x * self.square_size + self.start_x,
                            rev_y * self.square_size + self.start_y),
                        Point(
                            x * self.square_size + self.square_size + self.start_x,
                            rev_y * self.square_size + self.square_size+ self.start_y
                           ),
                        copy(color)))


    def on_draw(self):
        self.clear()
        for line in self.squares:
            for square in line:
                square.draw()
        # self.flip()

    def update(self, dt):
        return
        self.on_draw()


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.on_mouse_release(x, y, mouse.LEFT, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.solution_backup = deepcopy(self.game_board.solution)
        for i in range(self.game_board.rows):
            for j in range(self.game_board.cols):
                self.squares_backup[i][j] = self.squares[i][j].color
        if button == mouse.LEFT:
            self.pressed_cords = [(x - self.start_x)//self.square_size, (y - self.start_y)//self.square_size]

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.released_cords = [(x - self.start_x) // self.square_size, (y - self.start_y) // self.square_size]
            if self.released_cords[0] < 0 \
                    or self.released_cords[0] > self.game_board.cols - 1 \
                    or self.released_cords[1] < 0 \
                    or self.released_cords[1] > self.game_board.rows - 1:
                return # Todo method

            point1 = Point(
                min(self.pressed_cords[0], self.released_cords[0]),
                # min(self.pressed_cords[1], self.released_cords[1])
                min(self.game_board.cols - self.pressed_cords[1] - 1, self.game_board.cols - self.released_cords[1] - 1)
            )
            point2 = Point(
                max(self.pressed_cords[0], self.released_cords[0]),
                # max(self.pressed_cords[1], self.released_cords[1])
                max(self.game_board.cols - self.pressed_cords[1] - 1, self.game_board.cols - self.released_cords[1] - 1)
            )
            self.update_solution(point1, point2)


    def get_grid_cords(self):
        pass

    def on_key_press(self, KEY, MOD):
        if KEY == key.ESCAPE:
            tf = TextureFactory([self.game_board])
            tf.generate_single_texture(str(self.filename), self.game_board)
            self.parent.restart = True
            self.close()
            del self


    def update_solution(self, first_point: Point, second_point: Point):
        self.game_board.solution = deepcopy(self.solution_backup)
        for i in range(self.game_board.rows):
            for j in range(self.game_board.cols):
                self.squares[i][j].color = self.squares_backup[i][j]
        # first_point2 = first_point.clone()
        # second_point2 = second_point.clone()
        # first_point2.x = self.game_board.cols - first_point.x - 1
        # second_point2.x = self.game_board.cols - second_point.x - 1
        # if (second_point2.y < first_point2.y):
        #     t = second_point2.y
        #     second_point2.y = first_point2.y
        #     first_point2.y = t
        # rev_y = cols - y - 1
        # y = cols - rev_y - 1


        rect = Rectangle(self.game_board, first_point, second_point, 0)
        rect.color = rect.find_color()
        if rect.color == -1:
            color = (250, 190, 250)
        else:
            color = COLORS[rect.color % (len(COLORS) - 1)][0:3]
        rect.draw_rectangle()
        for x in range(rect.top_left.x, rect.bottom_right.x + 1):
            for y in range(rect.top_left.y, rect.bottom_right.y + 1):
                self.squares[self.game_board.cols - y - 1][x].color = color
        if self.game_board.verifySolution():
            print('zaebis')


class Square:
    def __init__(self, number: str, point1: Point, point2: Point, color):
        self.cords = [
            point1.x, point1.y,
            point2.x, point1.y,
            point2.x, point2.y,
            point1.x, point2.y
        ]
        self.color = deepcopy(color)
        self.label = pyglet.text.Label(
            number,
            font_name='Arial',
            font_size=20,
            color=(0, 0, 0, 255),
            x=(point1.x+point2.x)//2,
            y=(point1.y+point2.y)//2,
            anchor_x='center', anchor_y='center')

    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', self.cords),
                             ('c3B', self.color * int(len(self.cords)/2)))
        self.label.draw()
