import math
import pyglet
from pyglet.gl import *

from Utilities.texture_loader import get_texture


class Cube:
    def __init__(self, rotation: bool):
        self.i = 1.1
        self.rotation = rotation

        texture_filenames = [
            'Resources/textures/0.png',
            'Resources/textures/1.png',
            'Resources/textures/2.png',
            'Resources/textures/3.png',
            'Resources/textures/4.png',
            'Resources/textures/5.png'
        ]
        self.textures = list()
        for filename in texture_filenames:
            self.textures.append(get_texture(filename))

        self.batch = pyglet.graphics.Batch()
        x, y, z = -1, -1, -1
        X, Y, Z = 1, 1, 1
        self.sides = list()
        self.sides.append(self.batch.add(4, GL_QUADS, self.textures[0],
                                         ('v3f/dynamic', (
                                             x, y, z, x, y, Z, x, Y, Z, x, Y,
                                             z)),
                                         ('t2f/dynamic',
                                          (1, 0, 1, 1, 0, 1, 0, 0))))
        self.sides.append(self.batch.add(4, GL_QUADS, self.textures[1],
                                         ('v3f/dynamic', (
                                             X, y, z, X, y, Z, X, Y, Z, X, Y,
                                             z)),
                                         ('t2f/dynamic',
                                          (1, 0, 1, 1, 0, 1, 0, 0))))
        self.sides.append(self.batch.add(4, GL_QUADS, self.textures[2],
                                         ('v3f/dynamic', (
                                             x, y, Z, X, y, Z, X, Y, Z, x, Y,
                                             Z)),
                                         ('t2f/dynamic',
                                          (1, 0, 1, 1, 0, 1, 0, 0))))
        self.sides.append(self.batch.add(4, GL_QUADS, self.textures[3],
                                         ('v3f/dynamic', (
                                             x, y, z, X, y, z, X, Y, z, x, Y,
                                             z)),
                                         ('t2f/dynamic',
                                          (1, 0, 1, 1, 0, 1, 0, 0))))
        self.sides.append(self.batch.add(4, GL_QUADS, self.textures[4],
                                         ('v3f/dynamic', (
                                             x, y, z, x, y, Z, X, y, Z, X, y,
                                             z)),
                                         ('t2f/dynamic',
                                          (1, 0, 1, 1, 0, 1, 0, 0))))
        self.sides.append(self.batch.add(4, GL_QUADS, self.textures[5],
                                         ('v3f/dynamic', (
                                             x, Y, z, x, Y, Z, X, Y, Z, X, Y,
                                             z)),
                                         ('t2f/dynamic',
                                          (1, 0, 1, 1, 0, 1, 0, 0))))

    def draw(self):
        if not self.rotation:
            self.batch.draw()
            return
        x1 = math.cos(self.i)
        z1 = math.sin(self.i)
        x11 = math.sin(self.i)
        z11 = math.cos(self.i)
        x2 = -x1
        z2 = -z1
        x22 = -x11
        z22 = -z11
        # y1 = math.sin(self.i)
        # y2 = math.sin(self.i + math.pi/2)
        # y22 = -y1
        # y11 = -y2
        y11 = -math.sqrt(2) / 2
        y22 = math.sqrt(2) / 2
        y1 = -math.sqrt(2) / 2
        y2 = math.sqrt(2) / 2
        a = [x1, y1, z1]
        b = [x11, y11, z22]
        c = [x2, y1, z2]
        d = [x22, y11, z11]
        A = [x1, y2, z1]
        B = [x11, y22, z22]
        C = [x2, y2, z2]
        D = [x22, y22, z11]
        self.sides[0].vertices = b + B + A + a
        self.sides[1].vertices = d + D + C + c
        self.sides[2].vertices = c + C + B + b
        self.sides[3].vertices = a + A + D + d
        self.sides[4].vertices = a + d + c + b
        self.sides[5].vertices = A + B + C + D
        self.batch.draw()
        self.i += 0.01
        self.i %= 100
        # TODo Навести порядок, выделить методы
