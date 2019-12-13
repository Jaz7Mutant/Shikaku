import math
import pyglet
from pyglet.gl import *

from Utilities.texture_loader import get_texture


class Cube:
    def __init__(self, rotation: bool):
        self.i = 1.1
        self.rotation = rotation
        x, y, z = -1, -1, -1
        X, Y, Z = 1, 1, 1
        vertex_type = 'v3f/dynamic'
        vertices = [
            (vertex_type, (x, y, z, x, y, Z, x, Y, Z, x, Y, z)),
            (vertex_type, (X, y, z, X, y, Z, X, Y, Z, X, Y, z)),
            (vertex_type, (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z)),
            (vertex_type, (x, y, z, X, y, z, X, Y, z, x, Y, z)),
            (vertex_type, (x, y, z, x, y, Z, X, y, Z, X, y, z)),
            (vertex_type, (x, Y, z, x, Y, Z, X, Y, Z, X, Y, z))
        ]
        texture_anchors = ('t2f/dynamic', (1, 0, 1, 1, 0, 1, 0, 0))
        self.batch = pyglet.graphics.Batch()
        self.sides = list()
        for i in range(6):
            self.sides.append(
                self.batch.add(
                    4, GL_QUADS,
                    get_texture(f'Resources/textures/{i}.png'),
                    vertices[i], texture_anchors))

    def draw(self):
        if not self.rotation:
            self.batch.draw()
            return
        x1 = math.cos(self.i)
        x2 = -x1
        x11 = math.sin(self.i)
        x22 = -x11

        y1 = -math.sqrt(2) / 2
        y2 = -y1
        y11 = y1
        y22 = -y1

        # uncomment it just for fun
        # y1 = math.cos(self.i)
        # y2 = math.sin(self.i + math.pi/2) + math.sin(math.cos(self.i))
        # y22 = math.cos(self.i) + math.sin(self.i) - y2
        # y11 = math.sin(self.i)

        z1 = math.sin(self.i)
        z11 = math.cos(self.i)
        z2 = -z1
        z22 = -z11

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
        self.i %= 10
