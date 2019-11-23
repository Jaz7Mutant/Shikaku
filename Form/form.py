from pyglet.gl import *
from pyglet.window import key
import math
from Form.cube import Cube
from Form.interactive_field import InteractiveField


class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.i = 0.1

    def mouse_motion(self, dx, dy):  # todo Исправить
        dx /= 8
        dy /= 8
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0] > 90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    def update(self, dt, keys):
        s = dt * 10
        rotY = -self.rot[1] / 180 * math.pi
        dx, dz = s * math.sin(rotY), s * math.cos(rotY)
        if keys[key.W]: self.pos[0] += dx; self.pos[2] -= dz
        if keys[key.S]: self.pos[0] -= dx; self.pos[2] += dz
        if keys[key.A]: self.pos[0] -= dz; self.pos[2] -= dx
        if keys[key.D]: self.pos[0] += dz; self.pos[2] += dx

        if keys[key.SPACE]: self.pos[1] += s
        if keys[key.LSHIFT]: self.pos[1] -= s
        # TODO Исправить
        self.i += 0.01 # TODO Сделать общий счетчик?
        self.i %= 100


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.model = Cube(True)
        self.player = Player((0, 1.5, 1.5), (-30, 0))
        self.field = InteractiveField('Resources/textures/0.png', 3, 0, 0, 3.5, 0.5, 0)

    def push(self, pos, rot):
        glPushMatrix()
        glRotatef(-rot[0], 1, 0, 0);
        glRotatef(-rot[1], 0, 1, 0);
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
        # sleep(0.5)
        self.clear()
        self.set3d()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        self.push(self.player.pos, self.player.rot)
        self.model.draw()
        self.field.draw()
        glPopMatrix()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, (
            'v2f', [x, y, x - dx, y, x - dx, y - dy, x, y - dy]))


def main():
    window = Window(width=800, height=600, caption='Shikaku solver',
                    resizable=True)
    glClearColor(0.5, 0.7, 1, 1)
    pyglet.app.run()


if __name__ == '__main__':
    main()
