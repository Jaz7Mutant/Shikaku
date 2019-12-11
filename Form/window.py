from pyglet.gl import *
from pyglet.window import key
import math
from Form.cube import Cube
from Form.game import Game
from Form.interactive_field import InteractiveField
from Form.player import Player


class Window(pyglet.window.Window):
    def __init__(self, boards, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.model = Cube(True)
        self.player = Player((0, 1.5, 1.5), (-30, 0))
        self.fields = []
        self.boards = boards
        self.restart = False
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        for i in range(6):
            self.fields.append(InteractiveField(
                'Resources/textures/' + str(i) + '.png', i + 3, 0, 0, i + 3.5, 0.5, 0))

    def push(self, pos, rot):
        glPushMatrix()
        glRotatef(-rot[0], 1, 0, 0)
        glRotatef(-rot[1], 0, 1, 0)
        glTranslatef(-pos[0], -pos[1], -pos[2], )
        # gluLookAt(pos[0], pos[1], pos[2], 0, 0, 0, 0, 1, 0)

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        self.Projection()
        gluOrtho2D(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width / self.height, 0.05, 1000)
        self.Model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self: self.lock, setLock)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock: self.player.mouse_motion(dx, dy)

    def on_key_press(self, KEY, MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_draw(self):
        if self.restart:
            for field in self.fields:
                field.restart()
            self.model = Cube(True)
            self.restart = False
        # sleep(0.5)
        self.clear()
        self.set3d()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        self.push(self.player.pos, self.player.rot)
        self.model.draw()
        for field_num, field in enumerate(self.fields):
            if not field.check_intersection(self.player.pos):
                field.draw()
            else:
                self.player.pos = field.get_player_pos()
                self.keys.clear()
                # self.restart = True
                # glPopMatrix()
                # self.player.pos = [0,0,0]
                window2 = Game(field_num, self.boards[field_num], self, width=800, height=600,
                                caption='Shikaku solver field',
                                resizable=True)
                glClearColor(0.3, 0.8, 1, 1)
                # glClearDepth(1.0)
                pyglet.app.run()
                self.model = Cube(True)
                return

        glPopMatrix()




def main(boards):
    window = Window(boards, width=800, height=600, caption='Shikaku solver',
                    resizable=True)
    glClearColor(0.5, 0.7, 1, 1)
    # glClearDepth(1.0)
    pyglet.app.run()


if __name__ == '__main__':
    main([])
