from pyglet.gl import *

from Utilities.texture_loader import get_texture


class InteractiveField:
    def __init__(self, filename, x1, y1, z1, x2, y2, z2):
        self.texture = get_texture(filename)
        self.batch = pyglet.graphics.Batch()
        self.side = self.batch.add(
            4,
            GL_QUADS,
            self.texture,
            ('v3f', (x2, y1, z1, x2, y2, z1, x1, y2, z1, x1, y1, z1)),
            ('t2f/dynamic',
             (1, 0, 1, 1, 0, 1, 0, 0)))

    def draw(self):
        self.batch.draw()

    def check_intersection(self):
        pass
    # TODO
