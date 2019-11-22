from pyglet.gl import *
from pyglet.window import key
import math


class Model:
    def __init__(self):
        texture_filenames = ['textures/0.png',
                             'textures/1.png',
                             'textures/2.png',
                             'textures/3.png',
                             'textures/4.png',
                             'textures/5.png']
        self.textures = list()
        self.get_textures(texture_filenames)
        self.batch = pyglet.graphics.Batch()
        texture_coordinates = ('t2f', (1, 0, 1, 1, 0, 1, 0, 0,))
        x, y, z = 0, 0, -1
        X, Y, Z = x + 1, y + 1, z + 1
        self.batch.add(4, GL_QUADS, self.textures[0],
                       ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)),
                       texture_coordinates)
        self.batch.add(4, GL_QUADS, self.textures[1],
                       ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)),
                       texture_coordinates)
        self.batch.add(4, GL_QUADS, self.textures[2],
                       ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)),
                       texture_coordinates)
        self.batch.add(4, GL_QUADS, self.textures[3],
                       ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)),
                       texture_coordinates)
        self.batch.add(4, GL_QUADS, self.textures[4],
                       ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)),
                       texture_coordinates)
        self.batch.add(4, GL_QUADS, self.textures[5],
                       ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)),
                       texture_coordinates)

    def get_textures(self, filenames: list):
        for filename in filenames:
            img = pyglet.image.load(filename)
            texture = img.get_texture()
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            self.textures.append(pyglet.graphics.TextureGroup(texture))

    def draw(self):
        self.batch.draw()


class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.i = 0.1

    # def mouse_motion(self, dx, dy): # todo not implemented yet
    #     dx /= 8
    #     dy /= 8
    #     self.rot[0] += dy
    #     self.rot[1] -= dx
    #     if self.rot[0] > 90:
    #         self.rot[0] = 90
    #     elif self.rot[0] < -90:
    #         self.rot[0] = -90

    def update(self, dt, keys):
        # s = dt * 10
        # rotY = -self.rot[1] / 180 * math.pi
        # dx, dz = s * math.sin(rotY), s * math.cos(rotY)
        # if keys[key.W]: self.pos[0] += dx; self.pos[2] -= dz
        # if keys[key.S]: self.pos[0] -= dx; self.pos[2] += dz
        # if keys[key.A]: self.pos[0] -= dz; self.pos[2] -= dx
        # if keys[key.D]: self.pos[0] += dz; self.pos[2] += dx
        #
        # if keys[key.SPACE]: self.pos[1] += s
        # if keys[key.LSHIFT]: self.pos[1] -= s
        # TODO not implemented yet
        self.pos[0] = (math.sin(self.i) + 0.5) * 1.5
        self.pos[2] = (math.cos(self.i) - 0.5) * 1.5
        self.pos[1] = (math.cos(self.i) + math.sin(self.i)) * 1.5
        # self.i += 3.13
        self.i += 0.01


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.model = Model()
        self.player = Player((0, 1.5, 1.5), (-30, 0))

    def push(self, pos, rot):
        glPushMatrix()
        # glRotatef(-rot[0], 1, 0, 0); glRotatef(-rot[1], 0, 1,0); glTranslatef(-pos[0], -pos[1], -pos[2],)
        gluLookAt(pos[0], pos[1], pos[2], 0.5, 0.5, -0.5, 0, 1, 0)

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        self.Projection()
        gluOrtho2D(0, self.width, 0,self.height)
        self.Model()

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width / self.height, 0.05,1000)
        self.Model()

    # def setLock(self, state):
    #     self.lock = state
    #     self.set_exclusive_mouse(state)
    # lock = False
    # mouse_lock = property(lambda self: self.lock, setLock)



    # def on_mouse_motion(self, x, y, dx, dy):
    #     if self.mouse_lock: self.player.mouse_motion(dx, dy)

    # def on_key_press(self, KEY, MOD):
    #     if KEY == key.ESCAPE:
    #         self.close()
    #     elif KEY == key.E:
    #         self.mouse_lock = not self.mouse_lock

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        self.push(self.player.pos, self.player.rot)
        self.model.draw()
        glPopMatrix()


def main():
    # config = pyglet.gl.Config(sample_buffers=1, samples=4)
    window = Window(width=800, height=600, caption='Shikaku solver',
                    resizable=True)
    glClearColor(0.5, 0.7, 1, 1)
    pyglet.app.run()


if __name__ == '__main__':
    main()
