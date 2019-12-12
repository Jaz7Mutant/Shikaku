from copy import deepcopy

from pyglet.gl import *
from pyglet.window import key, mouse

from Form.square import Square
from Solver.game_board import GameBoard
from Utilities.point import Point
from Utilities.rectangle import Rectangle
from Utilities.texture_colors import COLORS
from Utilities.texture_factory import TextureFactory


def start(field_num: str, game_board: GameBoard):
    window = Game(field_num, game_board, width=800, height=600,
                  caption=f'puzzle #{field_num}', resizable=True)
    window.set_minimum_size(300, 200)
    glClearColor(0.3, 0.8, 1, 1)
    glClearDepth(1.0)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    pyglet.app.run()


class Game(pyglet.window.Window):
    def __init__(self, filename: str, game_board: GameBoard, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.filename = filename
        self.board = game_board
        self.pressed_cords = []
        self.released_cords = []

        self.squares_backup = [self.board.cols * [0]
                               for i in range(self.board.rows)]
        self.solution_backup = self.board.solution.copy()
        self.squares = [self.board.cols * [Square] for i in
                        range(self.board.rows)]
        self.cell_size = self.height // (self.board.cols + 1)
        self.start_x = self.cell_size // 2
        self.start_y = self.cell_size // 2
        self.initialize_board_model()

    def initialize_board_model(self):
        self.board.initialize_board_solution()
        colored_squares = 0
        for y, row in enumerate(self.board.board):
            for x, value in enumerate(row):
                rev_y = self.board.cols - y - 1
                color = (180, 210, 230)
                symbol = ' ' if value == -1 else str(value)
                if value != -1:
                    self.board.solution[y][x] = colored_squares
                    color = COLORS[int(self.board.solution[y][x])
                                   % (len(COLORS) - 1)][0:3]
                    colored_squares += 1

                self.squares[rev_y][x] = (Square(
                    symbol,
                    Point(
                        x * self.cell_size + self.start_x,
                        rev_y * self.cell_size + self.start_y),
                    Point(
                        x * self.cell_size + self.cell_size + self.start_x,
                        rev_y*self.cell_size + self.cell_size + self.start_y),
                    color))

    def on_draw(self):
        self.clear()
        for line in self.squares:
            for square in line:
                square.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.solution_backup = deepcopy(self.board.solution)
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                self.squares_backup[i][j] = self.squares[i][j].color
        if button == mouse.LEFT:
            self.pressed_cords = [(x - self.start_x) // self.cell_size,
                                  (y - self.start_y) // self.cell_size]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.on_mouse_release(x, y, mouse.LEFT, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.released_cords = [(x - self.start_x) // self.cell_size,
                                   (y - self.start_y) // self.cell_size]
            if not self.check_mouse_movement():
                return

            point1 = Point(
                min(self.pressed_cords[0], self.released_cords[0]),
                min(self.board.cols - self.pressed_cords[1] - 1,
                    self.board.cols - self.released_cords[1] - 1))
            point2 = Point(
                max(self.pressed_cords[0], self.released_cords[0]),
                max(self.board.cols - self.pressed_cords[1] - 1,
                    self.board.cols - self.released_cords[1] - 1))
            self.update_solution(point1, point2)

    def on_key_press(self, KEY, MOD):
        from Form.window import Window
        if KEY == key.ESCAPE:
            tf = TextureFactory([self.board])
            tf.generate_single_texture(str(self.filename), self.board)
            Window.RESTART = True
            self.close()
            del self

    def update_solution(self, first_point: Point, second_point: Point):
        self.board.solution = deepcopy(self.solution_backup)
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                self.squares[i][j].color = self.squares_backup[i][j]

        rect = Rectangle(self.board, first_point, second_point, 0)
        rect.find_color()
        color = (250, 190, 250) if rect.color == -1 \
            else COLORS[rect.color % (len(COLORS) - 1)][0:3]
        rect.draw_rectangle()

        for x in range(rect.top_left.x, rect.bottom_right.x + 1):
            for y in range(rect.top_left.y, rect.bottom_right.y + 1):
                self.squares[self.board.cols - y - 1][x].color = color
        self.check_solution()

    def check_mouse_movement(self) -> bool:
        return not (self.released_cords[0] < 0 or
                    self.released_cords[0] > self.board.cols - 1 or
                    self.released_cords[1] < 0 or
                    self.released_cords[1] > self.board.rows - 1)

    def check_solution(self):
        if self.board.verifySolution():
            label = pyglet.text.Label(
                'Congratulations!',
                font_name='Arial',
                font_size=40,
                color=(0, 0, 0, 255),
                x=self.width // 2,
                y=self.height // 2,
                anchor_x='center', anchor_y='center')
            label.draw()
