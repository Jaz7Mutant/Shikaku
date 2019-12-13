from typing import List

from pyglet.gl import *
from pyglet.window import key

from Form.game import start_game
from Form.cube import Cube
from Form.cube_face import CubeFace
from Form.player import Player
from Solver.game_board import GameBoard


def start(boards: List[GameBoard]):
    window = Window(boards, width=800, height=600, caption='Shikaku solver',
                    resizable=True)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glClearColor(0.5, 0.7, 1, 1)
    glClearDepth(1.0)
    window.set_minimum_size(300, 200)
    window.set_exclusive_mouse(True)
    window.set_mouse_visible(False)

    # Suppress .flip() exception while stopping event loop.
    # Only way to fix it is make a custom event loop, but there is no need
    try:
        pyglet.app.run()
    except AttributeError:
        pass


def push(pos, rot):
    glPushMatrix()
    glRotatef(-rot[0], 1, 0, 0)
    glRotatef(-rot[1], 0, 1, 0)
    glTranslatef(-pos[0], -pos[1], -pos[2])


def model():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()


class Window(pyglet.window.Window):
    def __init__(self, boards: List[GameBoard], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.boards = boards
        self.cube = Cube(True)
        self.player = Player((0, 1.5, 1.5), (-3, 0))
        self.cube_faces = []
        for i in range(6):
            self.cube_faces.append(CubeFace(
                'Resources/textures/' + str(i) + '.png',
                i + 3, 0, 0, i + 3.5, 0.5, 0))
        pyglet.clock.schedule(self.update)

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.mouse_motion(dx, dy)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.clock.unschedule(self.update)
            self.close()
            del self

    def on_draw(self):
        self.clear()
        self.set3d()
        push(self.player.pos, self.player.rot)
        self.cube.draw()
        for field_num, cube_face in enumerate(self.cube_faces):
            if not cube_face.check_intersection(self.player.pos):
                cube_face.draw()
            else:
                self.player.pos = cube_face.get_player_pos()
                self.keys.clear()
                start_game(str(field_num), self.boards[field_num], self.reload)
                return
        glPopMatrix()

    def reload(self):
        self.keys.clear()
        for cube_face in self.cube_faces:
            cube_face.restart()
        self.cube = Cube(True)

    def set3d(self):
        projection()
        gluPerspective(70, self.width / self.height, 0.01, 1000)
        model()

    def set2d(self):
        projection()
        gluOrtho2D(0, self.width, 0, self.height)
        model()
